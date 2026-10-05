from django.db import models

from apps.airport.models import Airport


class Airline(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2, unique=True)
    hub_airport = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True)
    # fleet =
