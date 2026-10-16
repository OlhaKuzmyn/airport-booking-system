from rest_framework import viewsets

from apps.flight.models import Flight
from apps.flight.serializers import FlightListSerializer, FlightDetailSerializer, FlightSerializer


class FlightViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Flight.objects.select_related(
            "origin_airport",
            "destination_airport",
            "airline"
        )
        if self.action == "retrieve":
            return queryset.prefetch_related("aircraft",
                                      "aircraft__aircraft_type",)
        if self.action == "list":
            return queryset
        return queryset.select_related("aircraft")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FlightDetailSerializer
        elif self.action == "list":
            return FlightListSerializer
        return FlightSerializer
