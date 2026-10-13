from django.urls import path, include
from rest_framework import routers

from apps.city.views import CityViewSet

router = routers.DefaultRouter()
router.register("cities", CityViewSet, basename="City")

urlpatterns = [
    path("", include(router.urls)),
]
