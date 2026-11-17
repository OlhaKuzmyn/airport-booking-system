from django.db import transaction
from django.utils import timezone
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
        past_booking = self.request.query_params.get("past_booking", None)
        queryset = Booking.objects.select_related(
                "user",
            )
        if past_booking:
            queryset = queryset.filter(flights__departure_date_time__lt=timezone.now())
        else:
            queryset = queryset.filter(flights__departure_date_time__gte=timezone.now())

        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                "flights", "passengers", "tickets"
            )
        return queryset.filter(user=self.request.user)
