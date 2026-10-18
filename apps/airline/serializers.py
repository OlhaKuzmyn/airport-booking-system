from rest_framework import serializers

from apps.aircraft.serializers import AircraftShortSerializer
from apps.airline.models import Airline


class AirlineSerializer(serializers.ModelSerializer):
    hub_airport = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Airline
        fields = (
            "id", "name", "code", "hub_airport"
        )


class AirlineDetailSerializer(AirlineSerializer):
    fleet = AircraftShortSerializer(read_only=True, many=True)

    class Meta:
        model = Airline
        fields = AirlineSerializer.Meta.fields + ("fleet",)
