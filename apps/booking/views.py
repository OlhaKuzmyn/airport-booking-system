from django.db import transaction
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.booking.models import Booking
from apps.booking.serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related("user").prefetch_related("tickets")
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
