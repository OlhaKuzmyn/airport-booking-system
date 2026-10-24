from django.db import models

from apps.flight.models import Flight
from apps.user.models import User


class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="bookings"
    )
    # outbound_flights = models.ManyToManyField(
    #     Flight,
    #     blank=True,
    #     null=True,
    #     related_name="bookings"
    # )
    # inbound_flights = models.ManyToManyField(
    #     Flight,
    #     blank=True,
    #     null=True,
    #     related_name="bookings"
    # )
    # outbound_flight_date = models.DateField()
    # inbound_flight_date = models.DateField()

    @property
    def passengers(self):

        return [
            f"{ticket.passenger.first_name} {ticket.passenger.last_name}"
            for ticket in self.tickets.all()
        ]

    # @property
    # def flight_date(self):
    #     set_flights = self.tickets.all()
