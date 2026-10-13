from django.db import models

from apps.city.models import City
from apps.country.models import Country


class Airport(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="airports"
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="airports"
    )
