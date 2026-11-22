import datetime
from zoneinfo import ZoneInfo

from django.utils import timezone
from rest_framework import serializers

from apps.flight.models import Flight, FlightNumber


class FlightNumberSerializer(serializers.ModelSerializer):
    origin_airport = serializers.SlugRelatedField(slug_field="code", read_only=True)
    destination_airport = serializers.SlugRelatedField(slug_field="code", read_only=True)
    airline = serializers.SlugRelatedField(slug_field="code", read_only=True)

    class Meta:
        model = FlightNumber
        fields = (
            "id", "airline", "number",
            "origin_airport", "destination_airport",
        )


class FlightSerializer(serializers.ModelSerializer):
    departure_date_time = serializers.DateTimeField()
    arrival_date_time = serializers.DateTimeField()

    class Meta:
        model = Flight
        fields = (
            "id", "flight_number", "aircraft",
            "departure_date_time", "arrival_date_time",
        )


    def validate(self, data):
        flt_num = data.get("flight_number") or self.instance.flight_number
        local_departure_timezone = flt_num.origin_airport.city.timezone
        local_arrival_timezone = flt_num.destination_airport.city.timezone
        departure_date_time = data.get("departure_date_time").replace(
            tzinfo=ZoneInfo(local_departure_timezone)
        ) or self.instance.departure_date_time
        arrival_date_time = data.get("arrival_date_time").replace(
            tzinfo=ZoneInfo(local_arrival_timezone)
        ) or self.instance.arrival_date_time


        if departure_date_time < timezone.now():
            raise serializers.ValidationError(
                "Departure date must not be in the past"
            )
        if arrival_date_time <= departure_date_time:
            raise serializers.ValidationError(
                "Arrival must be after departure"
            )
        data["departure_date_time"] = departure_date_time
        data["arrival_date_time"] = arrival_date_time

        return data

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        flt_num = instance.flight_number
        dep_tz = ZoneInfo(flt_num.origin_airport.city.timezone)
        arr_tz = ZoneInfo(flt_num.destination_airport.city.timezone)

        rep["departure_date_time"] = instance.departure_date_time.astimezone(dep_tz).isoformat()
        rep["arrival_date_time"] = instance.arrival_date_time.astimezone(arr_tz).isoformat()
        return rep


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
            "aircraft_number", "aircraft_type",
            "capacity", "current_availability", "duration", "past_flight"
        )

class FlightBookingSerializer(FlightListSerializer):

    class Meta:
        model = Flight
        fields = (
            "number", "origin_airport",
            "destination_airport","airline"
        )
