from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.aircraft_type.views import AircraftTypeViewSet

router = DefaultRouter()
router.register("aircraft-types", AircraftTypeViewSet, basename="AircraftType")

urlpatterns = [
    path("", include(router.urls)),
]