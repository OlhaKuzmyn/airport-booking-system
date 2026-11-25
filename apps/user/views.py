from django.db import transaction
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from airport_booking_system.services.email_service import EmailService
from airport_booking_system.services.jwt_service import JwtService, PasswordRecoveryToken, ActivateToken
from apps.user.models import User
from apps.user.serializers import UserSerializer, CheckEmailPasswordRecoverySerializer, RecoveryPasswordSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ActivateUserView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        token = kwargs.get("token")
        user = JwtService.validate_token(token, ActivateToken)
        user.is_active = True
        user.save(update_fields=["is_active"])
        return Response(status=status.HTTP_200_OK)


class CheckEmailPasswordRecoveryView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CheckEmailPasswordRecoverySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data["email"]).first()
        if user:
            EmailService.password_recovery(user)
        return Response(status=status.HTTP_200_OK)


class PasswordRecoveryView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RecoveryPasswordSerializer

    def post(self, request, *args, **kwargs):
        user = JwtService.validate_token(kwargs.get("token"), PasswordRecoveryToken)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data.get("password"))
        user.save(update_fields=["password"])
        return Response(status=status.HTTP_200_OK)
