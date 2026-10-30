from rest_framework import serializers

from apps.airport.models import Airport
from apps.flight.serializers import FlightBookingSerializer, FlightSerializer, FlightNumberSerializer


class AirportSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(slug_field="name", read_only=True)
    country = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Airport
        fields = ("id", "code", "name", "city", "country")

class AirportDepartingFlightSerializer(AirportSerializer):
    departing_flights = FlightNumberSerializer(many=True, read_only=True)

    class Meta:
        model = Airport
        fields = ("id", "code", "departing_flights",)

class AirportArrivingFlightSerializer(AirportSerializer):
    arriving_flights = FlightNumberSerializer(many=True, read_only=True)

    class Meta:
        model = Airport
        fields = ("id", "code", "arriving_flights",)
