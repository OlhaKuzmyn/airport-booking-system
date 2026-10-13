from rest_framework import viewsets, mixins

from apps.city.models import City
from apps.city.serializers import CitySerializer, CityDetailSerializer


class CityViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CityDetailSerializer
        return CitySerializer

    def get_queryset(self):
        if self.action == "retrieve":
            return City.objects.prefetch_related("country", "airports")
        return City.objects.select_related("country")
