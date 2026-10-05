from django.db import models

from apps.aircraft.models import Aircraft
from apps.airline.models import Airline
from apps.airport.models import Airport


class Flight(models.Model):
    number = models.CharField(max_length=5)
    origin_airport = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True)
    destination_airport = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True)
    airline = models.OneToOneField(Airline, on_delete=models.CASCADE)
    aircraft = models.OneToOneField(Aircraft, on_delete=models.SET_NULL, null=True)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
