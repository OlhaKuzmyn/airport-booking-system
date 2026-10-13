from rest_framework import viewsets, mixins

from apps.aircraft_type.models import AircraftType
from apps.aircraft_type.serializers import AircraftTypeSerializer


class AircraftTypeViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = AircraftType.objects.all()
    serializer_class = AircraftTypeSerializer
