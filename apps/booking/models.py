from django.db import models

from apps.passenger.models import Passenger
from apps.ticket.models import Ticket
from apps.user.models import User


class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="bookings"
    )
    passengers = models.ManyToManyField(Passenger, related_name="passengers")
    tickets = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True)
