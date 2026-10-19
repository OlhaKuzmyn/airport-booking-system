from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.booking.views import BookingViewSet

router = DefaultRouter()
router.register("bookings", BookingViewSet, basename="Booking")

urlpatterns = [
    path("", include(router.urls)),
]
