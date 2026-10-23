from rest_framework import serializers

from apps.flight.serializers import FlightSerializer
from apps.ticket.models import Ticket


class SeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = (
            "id", "seat_row_number", "seat_number"
        )
        read_only_fields = ("id",)

class TicketListSerializer(serializers.ModelSerializer):
    flights = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="number"
    )

    class Meta:
        model = Ticket
        fields = ("id", "flights", "date")