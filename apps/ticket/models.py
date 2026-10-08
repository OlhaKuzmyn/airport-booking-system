from django.db import models

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
        Flight, related_name="tickets", blank=True
    )
    date = models.DateField()
    seat_row_number = models.IntegerField()
    seat_number = models.IntegerField()
