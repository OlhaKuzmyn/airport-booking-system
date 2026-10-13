from rest_framework import serializers

from apps.city.models import City
from apps.country.serializers import CountrySerializer


class CitySerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = City
        fields = ("id", "name", "country")

class CityDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    airports = serializers.SlugRelatedField(slug_field="code", read_only=True, many=True)

    class Meta:
        model = City
        fields = ("id", "name", "country", "airports")