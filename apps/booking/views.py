from django.db import transaction
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.booking.models import Booking
from apps.booking.serializers import BookingSerializer, BookingListSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related("user").prefetch_related("tickets")
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return BookingListSerializer
        return BookingSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
