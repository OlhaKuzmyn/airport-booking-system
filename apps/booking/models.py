from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.flight.models import Flight
from apps.passenger.models import Passenger
from apps.user.models import User


class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="bookings"
    )
    outbound_flights = models.ManyToManyField(
        Flight,
        blank=True,
        related_name="bookings_outbound"
    )
    inbound_flights = models.ManyToManyField(
        Flight,
        blank=True,
        related_name="bookings_inbound"
    )
    outbound_flight_date = models.DateField(blank=True, null=True)
    inbound_flight_date = models.DateField(blank=True, null=True)
    number_of_passengers = models.IntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(9)],
    )
    passengers = models.ManyToManyField(
        Passenger,
        related_name="bookings",
    )
