from django.db import transaction
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.booking.models import Booking
from apps.booking.serializers import BookingSerializer, BookingListSerializer, BookingDetailSerializer


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return BookingListSerializer
        if self.action == "retrieve":
            return BookingDetailSerializer
        return BookingSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Booking.objects.select_related(
            "user",
        ).prefetch_related("outbound_flights", "inbound_flights", "passengers", "tickets")
        return queryset.filter(user=self.request.user)
