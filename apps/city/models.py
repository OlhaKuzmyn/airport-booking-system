from django.db import models
from timezonefinder import timezone_at

from apps.country.models import Country


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities"
    )
    longitude = models.FloatField()
    latitude = models.FloatField()

    @property
    def timezone(self):
        return timezone_at(lng=self.longitude, lat=self.latitude)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "country"],
                name="unique_city_name",
            )
        ]
