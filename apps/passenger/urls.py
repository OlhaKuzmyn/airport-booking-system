from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.passenger.views import PassengerViewSet

router = DefaultRouter()
router.register("passengers", PassengerViewSet, basename="Passenger")

urlpatterns = [
    path("", include(router.urls)),
]
