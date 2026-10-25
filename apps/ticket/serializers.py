from rest_framework import serializers

from apps.flight.serializers import FlightBookingSerializer
from apps.passenger.serializers import PassengerNameSerializer
from apps.ticket.models import Ticket


# class SeatSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Ticket
#         fields = (
#             "id", "seat_row_number", "seat_number"
#         )
#         read_only_fields = ("id",)

class TicketSerializer(serializers.ModelSerializer):
    passenger = PassengerNameSerializer(read_only=True)
    outbound_flight_date = serializers.DateField(format="%Y-%m-%d", read_only=True)
    inbound_flight_date = serializers.DateField(format="%Y-%m-%d", read_only=True)
    outbound_flights = FlightBookingSerializer(read_only=True, many=True)
    inbound_flights = FlightBookingSerializer(read_only=True, many=True)

    class Meta:
        model = Ticket
        fields = (
            "id", "passenger", "outbound_flight_date", "outbound_flights",
            "inbound_flight_date", "inbound_flights", "booking"
        )
