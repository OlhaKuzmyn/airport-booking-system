from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import transaction
from rest_framework import serializers

from apps.booking.models import Booking
from apps.flight.models import Flight
from apps.flight.serializers import FlightListSerializer, FlightBookingSerializer
from apps.passenger.models import Passenger
from apps.passenger.serializers import PassengerSerializer, PassengerNameSerializer
from apps.ticket.models import Ticket


class BookingSerializer(serializers.ModelSerializer):
    passengers = PassengerSerializer(many=True, required=False)
    booking_for_user = serializers.BooleanField(default=True, write_only=True)

    class Meta:
        model = Booking
        fields = ("id", "created_at", "passengers", "number_of_passengers",
                  "flights", "booking_for_user", "user"
                  )
        read_only_fields = ("id", "created_at", "user")

    def validate(self, attrs):
        number_of_passengers = attrs["number_of_passengers"]
        flights = attrs.get("flights", [])
        last_flight = None

        if flights:
            for flight in flights:
                if flight.current_availability < number_of_passengers:
                    raise serializers.ValidationError(
                        f"Not enough seats on the flight: {flight}"
                    )
                if last_flight is None:
                    last_flight = flight
                else:
                    if last_flight.arrival_date_time > flight.departure_date_time:
                        raise serializers.ValidationError(
                            f"Flight should not depart before arrival of {flight}"
                        )
                    else:
                        last_flight = flight
        else:
            raise serializers.ValidationError(
                "Please select at least one flight"
            )

        booking_for_user = attrs["booking_for_user"]
        passengers = attrs.get("passengers", [])

        if (booking_for_user and len(passengers) + 1 != number_of_passengers
        ) or (not booking_for_user and len(passengers) != number_of_passengers):
            raise serializers.ValidationError(
                "Number of passengers should be equal to passengers"
            )

        return attrs


    def create(self, validated_data):
        with transaction.atomic():
            passengers = validated_data.pop("passengers", [])
            flights = validated_data.pop("flights", [])
            booking_for_user = validated_data.pop("booking_for_user")
            user = self.context["request"].user
            booking = Booking.objects.create(**validated_data, user=user)
            if passengers:
                passengers = [Passenger.objects.create(**passenger) for passenger in passengers]
            if booking_for_user:
                passengers.extend([user.passenger])
            booking.passengers.set(passengers)
            booking.flights.set(flights)

            #TODO transaction not stopping booking creation in case of error!!!

            tickets = [Ticket.objects.create(
                passenger=passenger,
                booking=booking
                ) for passenger in passengers
            ]

            for ticket in tickets:
                ticket.flights.set(flights)
            return booking


class BookingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "id", "number_of_passengers",
            "created_at", "user")


class BookingDetailSerializer(BookingSerializer):
    passengers = PassengerSerializer(many=True, read_only=True)
    number_of_passengers = serializers.IntegerField(read_only=True)
    flights = FlightBookingSerializer(read_only=True, many=True)

    class Meta:
        model = Booking
        fields = BookingSerializer.Meta.fields + ("tickets",)
