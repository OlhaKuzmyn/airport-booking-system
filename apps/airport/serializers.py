from rest_framework import serializers

from apps.airport.models import Airport


class AirportSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(slug_field="name", read_only=True)
    country = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Airport
        fields = ("id", "code", "name", "city", "country")
