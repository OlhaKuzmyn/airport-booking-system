from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import transaction
from rest_framework import serializers

from apps.booking.models import Booking
from apps.flight.models import Flight
from apps.flight.serializers import FlightListSerializer, FlightBookingSerializer
from apps.passenger.models import Passenger
from apps.passenger.serializers import PassengerSerializer, PassengerNameSerializer
from apps.ticket.models import Ticket


class BookingSerializer(serializers.ModelSerializer):
    passengers = PassengerSerializer(many=True, required=False)
    booking_for_user = serializers.BooleanField(default=True, write_only=True)
    number_of_passengers = serializers.IntegerField()

    class Meta:
        model = Booking
        fields = ("id", "created_at", "passengers", "number_of_passengers",
                  "outbound_flights", "inbound_flights",
                  "booking_for_user", "user"
                  )
        read_only_fields = ("id", "created_at", "user")

    def validate(self, attrs):
        number_of_passengers = attrs["number_of_passengers"]
        flts = attrs.get("outbound_flights", []) + attrs.get("inbound_flights", [])
        for flight in flts:
            if flight.current_availability < number_of_passengers:
                raise serializers.ValidationError(
                    f"Not enough seats on the flight: {flight}"
                )
        return attrs


    def create(self, validated_data):
        with transaction.atomic():
            passengers = validated_data.pop("passengers", [])
            outbound_flights = validated_data.pop("outbound_flights", [])
            inbound_flights = validated_data.pop("inbound_flights", [])
            booking_for_user = validated_data.pop("booking_for_user")
            user = self.context["request"].user
            booking = Booking.objects.create(**validated_data, user=user)
            if passengers:
                passengers = [Passenger.objects.create(**passenger) for passenger in passengers]
            if booking_for_user:
                passengers.extend([user.passenger])
            booking.passengers.set(passengers)
            booking.outbound_flights.set(outbound_flights)
            booking.inbound_flights.set(inbound_flights)

            # print(len(passengers) == len(tickets_data))

            #TODO transaction not stopping booking creation in case of error!!!

            tickets = [Ticket.objects.create(
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


class BookingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "id", "number_of_passengers",
            "created_at", "user")


class BookingDetailSerializer(BookingSerializer):
    passengers = PassengerSerializer(many=True, read_only=True)
    number_of_passengers = serializers.IntegerField(read_only=True)
    outbound_flights = FlightBookingSerializer(read_only=True, many=True)
    inbound_flights = FlightBookingSerializer(read_only=True, many=True)

    class Meta:
        model = Booking
        fields = BookingSerializer.Meta.fields + ("tickets",)
