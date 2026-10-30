from django_filters import rest_framework as filters

from apps.flight.models import Flight


class FlightFilter(filters.FilterSet):
    origin_airport = filters.CharFilter(
        field_name="flight_number__origin_airport__code",
        lookup_expr="icontains"
    )
    destination_airport = filters.CharFilter(
        field_name="flight_number__destination_airport__code",
        lookup_expr="icontains"
    )
    airline = filters.CharFilter(
        field_name="flight_number__airline__code",
        lookup_expr="icontains"
    )
    departure_date = filters.DateFilter(
        field_name="departure_date_time",
        lookup_expr="date"
    )
    arrival_date = filters.DateFilter(
        field_name="arrival_date_time",
        lookup_expr="date"
    )
    departure_time_from = filters.TimeFilter(
        field_name="departure_date_time",
        lookup_expr="time__gte"
    )
    departure_time_by = filters.TimeFilter(
        field_name="departure_date_time",
        lookup_expr="time__lte"
    )
    arrival_time_from = filters.TimeFilter(
        field_name="arrival_date_time",
        lookup_expr="time__gte"
    )
    arrival_time_by = filters.TimeFilter(
        field_name="arrival_date_time",
        lookup_expr="time__lte"
    )
    aircraft_name = filters.CharFilter(
        field_name="aircraft__aircraft_type__name",
        lookup_expr="icontains"
    )


    class Meta:
        model = Flight
        fields = (
            "flight_number__origin_airport__code",
            "flight_number__destination_airport__code",
            "flight_number__airline__code",
            "departure_date_time", "arrival_date_time",
            "aircraft__aircraft_type__name",
        )
