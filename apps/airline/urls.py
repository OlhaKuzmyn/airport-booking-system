from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.airline.views import AirlineViewSet

router = DefaultRouter()
router.register("airlines", AirlineViewSet, basename="Airline")

urlpatterns = [
    path("", include(router.urls)),
]
