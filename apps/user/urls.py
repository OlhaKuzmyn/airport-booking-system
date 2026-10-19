from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.user.views import UserCreateView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("auth/", TokenObtainPairView.as_view(), name="authenticate"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="auth_refresh"),
]