from rest_framework import viewsets, mixins

from apps.aircraft.models import Aircraft
from apps.aircraft.serializers import AircraftSerializer


class AircraftViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Aircraft.objects.select_related("aircraft_type", "airline")
    serializer_class = AircraftSerializer
