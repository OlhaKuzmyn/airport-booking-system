from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from airport_booking_system.services.email_service import EmailService
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

    def create(self, validated_data):
        with transaction.atomic():
            dob = validated_data.pop("date_of_birth", None)
            user = get_user_model().objects.create_user(**validated_data)
            Passenger.objects.create(
                first_name=validated_data.get("first_name", ""),
                last_name=validated_data.get("last_name", ""),
                date_of_birth=dob,
                user=user,
            )
            EmailService.registration_confirmation(user)
            return user


class CheckEmailPasswordRecoverySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)


class RecoveryPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("password",)
        write_only_fields = ("password",)
