from rest_framework import viewsets, mixins

from apps.airline.models import Airline
from apps.airline.serializers import AirlineDetailSerializer, AirlineSerializer


class AirlineViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    def get_queryset(self):
        if self.action == "retrieve":
            return Airline.objects.select_related("hub_airport").prefetch_related("fleet")
        return Airline.objects.select_related("hub_airport")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AirlineDetailSerializer
        return AirlineSerializer
