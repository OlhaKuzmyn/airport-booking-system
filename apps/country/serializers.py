from rest_framework import serializers

from apps.country.models import Country


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ("id", "name")

class CountryDetailSerializer(serializers.ModelSerializer):
    cities = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Country
        fields = ("id", "name", "cities")