from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from apps.passenger.models import Passenger


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(
        write_only=True, required=False
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id", "email", "password",
            "first_name", "last_name", "date_of_birth",
            "is_staff", "is_active", "last_login",
            "is_superuser", "date_joined",
        )
        read_only_fields = (
            "id", "is_superuser", "is_staff", "is_active",
            "date_joined", "last_login"
        )
        extra_kwargs = {
            "password": {"write_only": True,}
        }

    # def validate(self, attrs):
    #     email = attrs["email"]
    #     password = attrs["password"]
    #     if email == password:
    #         raise serializers.ValidationError(
    #             {"email_eq_password": "email equals password"}
    #         )
    #     return attrs

    # @transaction.atomic
    def create(self, validated_data):
        with transaction.atomic():
            dob = validated_data.pop("date_of_birth")
            user = get_user_model().objects.create_user(**validated_data)
            user_passenger = {
                "first_name": validated_data["first_name"],
                "last_name": validated_data["last_name"],
                "date_of_birth": dob,
                "user": user,
            }
            Passenger.objects.create(**user_passenger)
            return user



