from django.db import models

from apps.booking.models import Booking
from apps.flight.models import Flight
from apps.passenger.models import Passenger


class Ticket(models.Model):
    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tickets"
    )
    flights = models.ManyToManyField(
        Flight,
        blank=True,
        related_name="tickets"
    )
    booking = models.ForeignKey(
        Booking,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tickets"
    )
