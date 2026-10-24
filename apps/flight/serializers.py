from rest_framework import serializers

from apps.flight.models import Flight


class FlightSerializer(serializers.ModelSerializer):
    departure_time = serializers.TimeField(format="%H:%M", input_formats=("%H:%M",))
    arrival_time = serializers.TimeField(format="%H:%M", input_formats=("%H:%M",))

    class Meta:
        model = Flight
        fields = (
            "id", "number", "origin_airport", "destination_airport",
            "airline", "aircraft", "departure_time", "arrival_time",
        )


class FlightListSerializer(FlightSerializer):
    origin_airport = serializers.SlugRelatedField(
        slug_field="code", read_only=True
    )
    destination_airport = serializers.SlugRelatedField(
        slug_field="code", read_only=True
    )
    airline = serializers.SlugRelatedField(
        slug_field="code", read_only=True
    )

    class Meta:
        model = Flight
        fields = (
            "id", "number", "origin_airport", "destination_airport",
            "airline", "departure_time", "arrival_time",
        )

class FlightDetailSerializer(FlightListSerializer):
    origin_airport = serializers.SlugRelatedField(
        slug_field="name", read_only=True
    )
    destination_airport = serializers.SlugRelatedField(
        slug_field="name", read_only=True
    )
    airline = serializers.SlugRelatedField(
        slug_field="name", read_only=True
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
            "aircraft_number", "aircraft_type", "capacity"
        )

class FlightBookingSerializer(FlightListSerializer):

    class Meta:
        model = Flight
        fields = (
            "number", "origin_airport",
            "destination_airport","airline"
        )
