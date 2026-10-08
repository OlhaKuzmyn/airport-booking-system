from django.db import models

from apps.aircraft.models import Aircraft
from apps.airport.models import Airport


class Airline(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2, unique=True)
    hub_airport = models.ForeignKey(
        Airport,
        on_delete=models.SET_NULL,
        null=True,
        related_name="hub_airlines"
    )
    fleet = models.ForeignKey(
        Aircraft,
        on_delete=models.SET_NULL,
        null=True
    )
