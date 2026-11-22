from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.user.views import UserCreateView, ActivateUserView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("auth/", TokenObtainPairView.as_view(), name="authenticate"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="auth_refresh"),
    path("activate/<str:token>", ActivateUserView.as_view(), name="activate_user"),
]