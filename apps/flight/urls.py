from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.flight.views import FlightViewSet

router = DefaultRouter()
router.register("flights", FlightViewSet, basename="Flight")

urlpatterns = [
    path("", include(router.urls)),
]
