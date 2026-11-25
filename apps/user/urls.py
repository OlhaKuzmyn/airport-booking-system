from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.user.views import UserCreateView, ActivateUserView, CheckEmailPasswordRecoveryView, PasswordRecoveryView, \
    ManageUserView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("manage-user/<int:id>/", ManageUserView.as_view(), name="manage_user"),
    path("auth/", TokenObtainPairView.as_view(), name="authenticate"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="auth_refresh"),
    path("activate/<str:token>/", ActivateUserView.as_view(), name="activate_user"),
    path("check-email/", CheckEmailPasswordRecoveryView.as_view(), name="check_email"),
    path("password-recovery/<str:token>/", PasswordRecoveryView.as_view(), name="password_recovery")
]
