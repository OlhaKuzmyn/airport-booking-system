from django.utils import timezone
from rest_framework import viewsets

from airport_booking_system.permissions import IsAdminOrReadOnly
from apps.flight.filters import FlightFilter
from apps.flight.models import Flight
from apps.flight.serializers import FlightListSerializer, FlightDetailSerializer, FlightSerializer


class FlightViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = FlightFilter

    def get_queryset(self):
        past_flight = self.request.query_params.get("past_flight", None)

        queryset = Flight.objects.select_related(
            "flight_number", "flight_number__airline",
            "flight_number__origin_airport__city",
            "flight_number__destination_airport__city",
        )
        if past_flight:
            queryset = queryset.filter(departure_date_time__lt=timezone.now())
        else:
            queryset = queryset.filter(departure_date_time__gte=timezone.now())

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
