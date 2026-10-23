from django.db import transaction
from rest_framework import serializers

from apps.booking.models import Booking
from apps.passenger.models import Passenger
from apps.passenger.serializers import PassengerSerializer
from apps.ticket.models import Ticket
from apps.ticket.serializers import SeatSerializer, TicketListSerializer


class BookingSerializer(serializers.ModelSerializer):
    passengers = PassengerSerializer(many=True, write_only=True)
    seats = SeatSerializer(many=True, write_only=True)
    flights = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    date = serializers.DateField(format="%Y-%m-%d", write_only=True)

    class Meta:
        model = Booking
        fields = ("id", "created_at", "passengers",
                  "flights", "date", "seats"
                  )
        read_only_fields = ("id", "created_at",)

    def create(self, validated_data):
        with (transaction.atomic()):
            passengers_data = validated_data.pop("passengers")
            flights = validated_data.pop("flights")
            date = validated_data.pop("date")
            seats = validated_data.pop("seats")
            user = self.context["request"].user
            booking = Booking.objects.create(**validated_data, user=user)
            passengers = [Passenger.objects.create(**passenger) for passenger in passengers_data]
            passengers.extend([user.passenger])

            # print(len(passengers) == len(tickets_data))

            #TODO transaction not stopping booking creation in case of error!!!

            tickets = [Ticket.objects.create(
                seat_row_number=seat["seat_row_number"],
                seat_number=seat["seat_number"],
                date=date, passenger=passenger, booking=booking
                ) for seat, passenger in zip(seats, passengers)
            ]

            for ticket in tickets:
                ticket.flights.set(flights)
            return booking


class BookingListSerializer(BookingSerializer):
    # passengers = PassengerSerializer(
    #     many=True, read_only=True, source="tickets.passengers"
    # )
    # flights = FlightSerializer(
    #     many=True, read_only=True, source="tickets.flights"
    # )
    # date = serializers.DateField(
    #     format="%Y-%m-%d", read_only=True, source="tickets.date"
    # )
    tickets = TicketListSerializer(many=True, read_only=True)
    #TODO make flight and date appear only once!!!

    class Meta:
        model = Booking
        fields = ("id", "created_at", "passengers", "tickets")
