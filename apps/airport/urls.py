from django.urls import path, include
from rest_framework import routers

from apps.airport.views import AirportViewSet

router = routers.DefaultRouter()
router.register("airports", AirportViewSet, basename="Airport")

urlpatterns = [
    path("", include(router.urls)),
]
