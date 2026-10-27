from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.flight.models import Flight
from apps.passenger.models import Passenger
from apps.user.models import User


class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="bookings"
    )
    flights = models.ManyToManyField(
        Flight,
        blank=True,
        related_name="bookings"
    )
    number_of_passengers = models.IntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(9)],
    )
    passengers = models.ManyToManyField(
        Passenger,
        related_name="bookings",
    )

    # @staticmethod
    # def validate_number_of_passengers(
    #         number_of_passengers, outbound_flights, inbound_flights, error
    # ):
    #     flights = outbound_flights.all().union(inbound_flights.all())
    #     for flight in flights:
    #         if flight.current_capacity >= number_of_passengers:
    #             flight.current_capacity -= number_of_passengers
    #         else:
    #             raise error(
    #                 {
    #                     f"Not enough seats on the flight: {flight}"
    #                 }
    #             )
    #
    # def clean(self):
    #     Booking.validate_number_of_passengers(
    #         self.number_of_passengers,
    #         self.outbound_flights,
    #         self.inbound_flights,
    #         ValueError
    #     )
    #
    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     return super(Booking, self).save(*args, **kwargs)



