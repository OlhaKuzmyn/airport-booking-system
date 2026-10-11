from rest_framework import viewsets, mixins

from apps.city.models import City
from apps.city.serializers import CitySerializer, CityDetailSerializer


class CityViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = City.objects.select_related("country")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CityDetailSerializer
        return CitySerializer
