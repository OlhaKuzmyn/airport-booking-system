from django.db import models

from apps.aircraft.models import Aircraft
from apps.airline.models import Airline
from apps.airport.models import Airport


class Flight(models.Model):
    number = models.CharField(max_length=5)
    origin_airport = models.ForeignKey(
        Airport,
        on_delete=models.SET_NULL,
        null=True,
        related_name="departing_flights"
    )
    destination_airport = models.ForeignKey(
        Airport,
        on_delete=models.SET_NULL,
        null=True,
        related_name="arriving_flights"
    )
    airline = models.ForeignKey(
        Airline,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    aircraft = models.ForeignKey(
        Aircraft,
        on_delete=models.SET_NULL,
        null=True,
        related_name="flights"
    )
    departure_time = models.TimeField()
    arrival_time = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["number", "airline"],
                name="unique_flight_airline_number"
            )
        ]
