from django.urls import path

from apps.user.views import UserCreateView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
]