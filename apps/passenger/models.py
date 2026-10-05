from django.db import models

from apps.user.models import User


class Passenger(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
