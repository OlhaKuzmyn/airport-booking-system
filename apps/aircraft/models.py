from django.db import models

from apps.aircraft_type.models import AircraftType
from apps.airline.models import Airline


class Aircraft(models.Model):
    serial_number = models.CharField(
        max_length=30, unique=True
    )
    aircraft_type = models.ForeignKey(
        AircraftType,
        on_delete=models.CASCADE,
    )
    airline = models.ForeignKey(
        Airline,
        on_delete=models.SET_NULL,
        null=True,
        related_name="fleet"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["serial_number", "aircraft_type"],
                name="unique_aircraft_serial_number"
            )
        ]
