from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from airport_booking_system.services.jwt_service import JwtActivateService
from apps.user.serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ActivateUserView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        token = kwargs.get("token")
        user = JwtActivateService.validate_token(token)
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK)
