from rest_framework import serializers

from apps.aircraft.models import Aircraft


class AircraftSerializer(serializers.ModelSerializer):
    aircraft_type = serializers.SlugRelatedField(read_only=True, slug_field="name")
    capacity = serializers.IntegerField(read_only=True, source="aircraft_type.capacity")

    class Meta:
        model = Aircraft
        fields = ("id", "serial_number", "aircraft_type", "capacity")
