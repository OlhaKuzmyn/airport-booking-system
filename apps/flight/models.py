from django.db import models

from apps.aircraft.models import Aircraft
from apps.airline.models import Airline
from apps.airport.models import Airport


class FlightNumber(models.Model):
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["number", "airline"],
                name="unique_flight_airline_number"
            )
        ]


class Flight(models.Model):
    flight_number = models.ForeignKey(
        FlightNumber,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    aircraft = models.ForeignKey(
        Aircraft,
        on_delete=models.SET_NULL,
        null=True,
        related_name="flights"
    )
    departure_date_time = models.DateTimeField()
    arrival_date_time = models.DateTimeField()


    def __str__(self):
        return f"{self.flight_number.airline.code} {self.flight_number.number}"


    @property
    def current_capacity(self):
        return self.aircraft.aircraft_type.capacity


