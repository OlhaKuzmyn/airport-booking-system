from rest_framework import serializers

from apps.passenger.models import Passenger


class PassengerSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(required=False)

    class Meta:
        model = Passenger
        fields = ("id", "first_name", "last_name", "date_of_birth")


class PassengerDetailSerializer(PassengerSerializer):
    user_email = serializers.EmailField(
        source="user.email", read_only=True
    )

    class Meta:
        model = Passenger
        fields = (
            "id", "first_name", "last_name", "date_of_birth", "user_email"
        )
