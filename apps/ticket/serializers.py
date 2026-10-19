from rest_framework import serializers

from apps.ticket.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    #TODO redo the serializer as no point in creating
    # a flight date in each ticket if its the same for several
    # tickets in booking
    #TODO consider if flights is causing a value error

    class Meta:
        model = Ticket
        fields = (
            "id", "flights", "date", "seat_row_number", "seat_number"
        )
        read_only_fields = ("id",)