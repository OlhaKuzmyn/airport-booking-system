from django.db import models


class AircraftType(models.Model):
    name = models.CharField(max_length=255)
    seat_rows = models.IntegerField()
    seat_columns = models.IntegerField()
