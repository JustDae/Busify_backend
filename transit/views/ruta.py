# transit/views/ruta.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from transit.models import Ruta
from transit.serializers.ruta import RutaSerializer
from transit.permissions import IsStaffOrReadOnly
from transit.filters import RutaFilter 
from transit.pagination import StandardPagination


class RutaViewSet(viewsets.ModelViewSet):
    queryset           = Ruta.objects.all()
    serializer_class   = RutaSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = RutaFilter 
    
    search_fields      = ['name', 'origin', 'destination', 'description']
    ordering_fields    = ['name', 'created_at', 'base_fare']
    ordering           = ['name']

    @action(detail=True, methods=['get'], url_path='paradas')
    def active_paradas(self, request, pk=None):
        from transit.serializers.parada import ParadaSummarySerializer
        
        ruta = self.get_object()
        qs   = ruta.paradas.filter(is_active=True).order_by('sequence')
        page = self.paginate_queryset(qs)
        
        if page is not None:
            return self.get_paginated_response(
                ParadaSummarySerializer(page, many=True).data
            )
        return Response(ParadaSummarySerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Ruta.objects.annotate(num_paradas=Count('paradas', distinct=True))
        
        return Response({
            'total':    qs.count(),
            'active':   qs.filter(is_active=True).count(),
            'inactive': qs.filter(is_active=False).count(),
            'detail': [
                {
                    'id':          r.id,
                    'name':        r.name,
                    'origin':      r.origin,      
                    'destination': r.destination, 
                    'base_fare':   r.base_fare,
                    'num_paradas': r.num_paradas,
                    'is_active':   r.is_active,
                }
                for r in qs.order_by('name')
            ],
        })