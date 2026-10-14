from django.db import models

from apps.aircraft_type.models import AircraftType


class Aircraft(models.Model):
    serial_number = models.CharField(
        max_length=255, unique=True
    )
    aircraft_type = models.ForeignKey(
        AircraftType,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["serial_number", "aircraft_type"],
                name="unique_aircraft_serial_number"
            )
        ]
