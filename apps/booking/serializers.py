from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import transaction
from rest_framework import serializers

from apps.booking.models import Booking
from apps.flight.serializers import FlightListSerializer, FlightBookingSerializer
from apps.passenger.models import Passenger
from apps.passenger.serializers import PassengerSerializer, PassengerNameSerializer
from apps.ticket.models import Ticket
from apps.ticket.serializers import SeatSerializer, TicketListSerializer


class BookingSerializer(serializers.ModelSerializer):
    passengers = PassengerSerializer(many=True)
    outbound_flight_date = serializers.DateField(format="%Y-%m-%d", required=False)
    inbound_flight_date = serializers.DateField(format="%Y-%m-%d", required=False)
    booking_for_user = serializers.BooleanField(default=True, write_only=True)
    number_of_passengers = serializers.IntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(9)
    ])

    class Meta:
        model = Booking
        fields = ("id", "created_at", "passengers", "number_of_passengers",
                  "outbound_flight_date", "inbound_flight_date",
                  "outbound_flights", "inbound_flights",
                  "booking_for_user", "user"
                  )
        read_only_fields = ("id", "created_at", "user")

    def create(self, validated_data):
        with transaction.atomic():
            passengers_data = validated_data.pop("passengers")
            outbound_flights = validated_data.pop("outbound_flights", None)
            inbound_flights = validated_data.pop("inbound_flights", None)
            outbound_flight_date = validated_data.get("outbound_flight_date", None)
            inbound_flight_date = validated_data.get("inbound_flight_date", None)
            booking_for_user = validated_data.pop("booking_for_user")
            user = self.context["request"].user
            booking = Booking.objects.create(**validated_data, user=user)
            passengers = [Passenger.objects.create(**passenger) for passenger in passengers_data]
            if booking_for_user:
                passengers.extend([user.passenger])
            booking.passengers.set(passengers)
            booking.outbound_flights.set(outbound_flights)
            booking.inbound_flights.set(inbound_flights)

            # print(len(passengers) == len(tickets_data))

            #TODO transaction not stopping booking creation in case of error!!!

            tickets = [Ticket.objects.create(
                outbound_flight_date=outbound_flight_date,
                inbound_flight_date=inbound_flight_date,
                passenger=passenger,
                booking=booking
                ) for passenger in passengers
            ]

            for ticket in tickets:
                if outbound_flights:
                    ticket.outbound_flights.set(outbound_flights)
                if inbound_flights:
                    ticket.inbound_flights.set(inbound_flights)
            return booking


class BookingListSerializer(BookingSerializer):
    passengers = PassengerNameSerializer(many=True, read_only=True)
    number_of_passengers = serializers.IntegerField(read_only=True)
    outbound_flights = FlightBookingSerializer(read_only=True, many=True)
    inbound_flights = FlightBookingSerializer(read_only=True, many=True)

    class Meta:
        model = Booking
        fields = (
            "id", "outbound_flights","outbound_flight_date",
            "inbound_flights", "inbound_flight_date",
            "passengers", "number_of_passengers",
            "created_at", "user")
