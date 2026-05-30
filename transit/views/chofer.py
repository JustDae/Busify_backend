# transit/views/chofer.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from transit.models import Chofer
from transit.serializers.chofer import ChoferSerializer
from transit.permissions import IsStaffOrReadOnly
from transit.pagination import StandardPagination


class ChoferViewSet(viewsets.ModelViewSet):
    queryset           = Chofer.objects.all()
    serializer_class   = ChoferSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ['is_active']
    search_fields      = ['first_name', 'last_name', 'license_number']
    ordering_fields    = ['last_name', 'first_name']
    ordering           = ['last_name']

    @action(detail=True, methods=['get'], url_path='viajes')
    def active_viajes(self, request, pk=None):
        from transit.models import Viaje
        from transit.serializers.viaje import ViajeSerializer 
        
        chofer = self.get_object()
        qs   = chofer.viaje_set.filter(estado='in_transit').order_by('-id')
        page = self.paginate_queryset(qs)
        
        if page is not None:
            return self.get_paginated_response(
                ViajeSerializer(page, many=True).data
            )
        return Response(ViajeSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Chofer.objects.annotate(num_viajes=Count('viaje', distinct=True))
        
        return Response({
            'total':         qs.count(),
            'active_staff':  qs.filter(is_active=True).count(),
            'inactive_staff':qs.filter(is_active=False).count(),
            'detail': [
                {
                    'id':             c.id,
                    'first_name':     c.first_name,
                    'last_name':      c.last_name,
                    'license_number': c.license_number,
                    'num_viajes':     c.num_viajes,
                    'is_active':      c.is_active,
                }
                for c in qs.order_by('last_name')
            ],
        })