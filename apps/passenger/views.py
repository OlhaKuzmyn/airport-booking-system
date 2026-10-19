from rest_framework import viewsets

from apps.passenger.models import Passenger
from apps.passenger.serializers import PassengerSerializer, PassengerDetailSerializer


class PassengerViewSet(viewsets.ModelViewSet):
    # change to create update destroy list only for passengers in booking not all passengers

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PassengerDetailSerializer
        return PassengerSerializer

    def get_queryset(self):
        if self.action == "retrieve":
            Passenger.objects.select_related("user")
        return Passenger.objects.all()
