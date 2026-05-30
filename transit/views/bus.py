# transit/views/bus.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from transit.models import Bus
from transit.serializers.bus import BusSerializer
from transit.permissions import IsStaffOrReadOnly
from transit.pagination import StandardPagination


class BusViewSet(viewsets.ModelViewSet):
    queryset           = Bus.objects.all()
    serializer_class   = BusSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ['status']
    search_fields      = ['unit_number', 'plate', 'model']
    ordering_fields    = ['unit_number', 'model']
    ordering           = ['unit_number']

    @action(detail=True, methods=['get'], url_path='viajes')
    def active_viajes(self, request, pk=None):
        from transit.models import Viaje
        from transit.serializers.viaje import ViajeSerializer 
        
        bus = self.get_object()
        
        qs   = bus.viaje_set.filter(status='en_route').order_by('-id')
        page = self.paginate_queryset(qs)
        
        if page is not None:
            return self.get_paginated_response(
                ViajeSerializer(page, many=True).data
            )
        return Response(ViajeSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Bus.objects.annotate(num_viajes=Count('viaje', distinct=True))
        
        return Response({
            'total':    qs.count(),
            'active':   qs.filter(status='active').count(),     
            'inactive': qs.filter(status='inactive').count(),
            'detail': [
                {
                    'id':          b.id,
                    'unit_number': b.unit_number,
                    'plate':       b.plate,
                    'model':       b.model,
                    'num_viajes':  b.num_viajes,
                    'status':      b.status,
                }
                for b in qs.order_by('unit_number')
            ],
        })