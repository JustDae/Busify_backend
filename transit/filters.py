import django_filters
from transit.models import Ruta, Parada, Viaje, Cooperativa


class CooperativaFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model  = Cooperativa
        fields = ['is_active']


class RutaFilter(django_filters.FilterSet):
    name     = django_filters.CharFilter(lookup_expr='icontains')
    fare_min = django_filters.NumberFilter(field_name='base_fare', lookup_expr='gte')
    fare_max = django_filters.NumberFilter(field_name='base_fare', lookup_expr='lte')

    class Meta:
        model  = Ruta
        fields = ['is_active', 'origin', 'destination']


class ParadaFilter(django_filters.FilterSet):
    name         = django_filters.CharFilter(lookup_expr='icontains')
    distance_min = django_filters.NumberFilter(field_name='distance', lookup_expr='gte')
    distance_max = django_filters.NumberFilter(field_name='distance', lookup_expr='lte')
    sequence_min = django_filters.NumberFilter(field_name='sequence', lookup_expr='gte')
    sequence_max = django_filters.NumberFilter(field_name='sequence', lookup_expr='lte')
    ruta_name    = django_filters.CharFilter(
        field_name='ruta__name', lookup_expr='icontains'
    )

    class Meta:
        model  = Parada
        fields = ['is_active', 'ruta']


class ViajeFilter(django_filters.FilterSet):
    from_date      = django_filters.DateFilter(field_name='departure_time', lookup_expr='date__gte')
    to_date        = django_filters.DateFilter(field_name='departure_time', lookup_expr='date__lte')
    passengers_min = django_filters.NumberFilter(field_name='passenger_count', lookup_expr='gte')
    passengers_max = django_filters.NumberFilter(field_name='passenger_count', lookup_expr='lte')

    class Meta:
        model  = Viaje
        fields = ['status', 'ruta', 'bus', 'chofer']