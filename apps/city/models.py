from django.db import models

from apps.country.models import Country


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "country"],
                name="unique_city_name",
            )
        ]
