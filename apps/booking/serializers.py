from django.db import transaction
from rest_framework import serializers

from apps.booking.models import Booking
from apps.passenger.models import Passenger
from apps.passenger.serializers import PassengerSerializer
from apps.ticket.models import Ticket
from apps.ticket.serializers import TicketSerializer


class BookingSerializer(serializers.ModelSerializer):
    passengers = PassengerSerializer(many=True)
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Booking
        fields = ("id", "created_at", "passengers", "tickets")
        read_only_fields = ("id", "created_at",)

    def create(self, validated_data):
        with (transaction.atomic()):
            passengers_data = validated_data.pop("passengers")
            tickets_data = validated_data.pop("tickets")
            user = self.context["request"].user
            booking = Booking.objects.create(**validated_data, user=user)
            passengers = [Passenger.objects.create(**passenger) for passenger in passengers_data]
            passengers.extend([user.passenger])

            # print(len(passengers) == len(tickets_data))

            for ticket, passenger in (tickets_data, passengers): #TODO ValueError: too many values to unpack (expected 2, got 3)
                Ticket.objects.create(**ticket, passenger=passenger, booking=booking)
