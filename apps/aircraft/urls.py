from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.aircraft.views import AircraftViewSet

router = DefaultRouter()
router.register("aircraft", AircraftViewSet, basename="Aircraft")

urlpatterns = [
    path("", include(router.urls)),
]
