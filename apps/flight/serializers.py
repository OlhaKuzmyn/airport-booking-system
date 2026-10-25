from rest_framework import serializers

from apps.flight.models import Flight


class FlightSerializer(serializers.ModelSerializer):
    departure_date_time = serializers.DateTimeField()
    arrival_date_time = serializers.DateTimeField

    class Meta:
        model = Flight
        fields = (
            "id", "flight_number", "aircraft",
            "departure_date_time", "arrival_date_time",
        )


class FlightListSerializer(FlightSerializer):
    origin_airport = serializers.CharField(
        source="flight_number.origin_airport.code",
        read_only=True
    )
    destination_airport = serializers.CharField(
        source="flight_number.destination_airport.code",
        read_only=True
    )
    airline = serializers.CharField(
        source="flight_number.airline.code", read_only=True
    )
    number = serializers.CharField(
        source="flight_number.number", read_only=True
    )

    class Meta:
        model = Flight
        fields = (
            "id", "number", "origin_airport", "destination_airport",
            "airline", "departure_date_time", "arrival_date_time",
        )

class FlightDetailSerializer(FlightListSerializer):
    origin_airport = serializers.CharField(
        source="flight_number.origin_airport.name",
        read_only=True
    )
    destination_airport = serializers.CharField(
        source="flight_number.destination_airport.name",
        read_only=True
    )
    airline = serializers.CharField(
        source="flight_number.airline.name",
        read_only=True
    )
    aircraft_number = serializers.CharField(
        source="aircraft.serial_number",
        read_only=True,
    )
    aircraft_type = serializers.CharField(
        source="aircraft.aircraft_type.name",
        read_only=True,
    )
    capacity = serializers.IntegerField(
        source="aircraft.aircraft_type.capacity",
        read_only=True,
    )


    class Meta:
        model = Flight
        fields = FlightListSerializer.Meta.fields + (
            "aircraft_number", "aircraft_type", "capacity", "current_availability"
        )

class FlightBookingSerializer(FlightListSerializer):

    class Meta:
        model = Flight
        fields = (
            "number", "origin_airport",
            "destination_airport","airline"
        )
