from rest_framework import serializers

from apps.aircraft_type.models import AircraftType


class AircraftTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AircraftType
        fields = ("id", "name", "seat_rows", "seat_columns", "capacity")
