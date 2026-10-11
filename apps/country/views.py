from rest_framework import viewsets, mixins

from apps.country.models import Country
from apps.country.serializers import CountrySerializer, CountryDetailSerializer


class CountryViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Country.objects.all()

    def get_queryset(self):
        if self.action == "retrieve":
            return Country.objects.prefetch_related("cities")
        return Country.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CountryDetailSerializer
        return CountrySerializer
