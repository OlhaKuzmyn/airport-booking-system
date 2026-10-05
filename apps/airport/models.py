from django.db import models

from apps.city.models import City


class Airport(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
