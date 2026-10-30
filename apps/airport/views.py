from rest_framework import viewsets, mixins

from apps.airport.models import Airport
from apps.airport.serializers import (
    AirportSerializer,
    AirportDepartingFlightSerializer, AirportArrivingFlightSerializer
)


class AirportViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    def flights(self):
        return self.request.query_params.get("flights").lower()

    def get_queryset(self):
        queryset = Airport.objects.prefetch_related("city", "country")
        if self.action == "retrieve":
            if self.flights() == "departing":
                return queryset.prefetch_related("departing_flights")
            elif self.flights() == "arriving":
                return queryset.prefetch_related("arriving_flights")
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            if self.flights() == "departing":
                return AirportDepartingFlightSerializer
            elif self.flights() == "arriving":
                return AirportArrivingFlightSerializer
        return AirportSerializer
