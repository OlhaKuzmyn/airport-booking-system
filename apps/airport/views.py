from rest_framework import viewsets, mixins

from apps.airport.models import Airport
from apps.airport.serializers import AirportSerializer


class AirportViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Airport.objects.prefetch_related("city", "country")
    serializer_class = AirportSerializer
