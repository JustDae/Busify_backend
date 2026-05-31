from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Max, Min, Sum, Count 
from transit.models import Cooperativa
from transit.serializers.cooperativa import CooperativaSerializer
from transit.permissions import IsStaffOrReadOnly
from transit.pagination import StandardPagination

class CooperativaViewSet(viewsets.ModelViewSet):

    queryset           = Cooperativa.objects.prefetch_related('rutas').all()
    serializer_class   = CooperativaSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ['is_active']
    
    search_fields      = ['name']
    ordering_fields    = ['name', 'created_at']
    ordering           = ['name']

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdminUser],
        url_path='toggle-status', 
    )
    def toggle_status(self, request, pk=None):
        cooperativa = self.get_object()
        try:
            is_active = request.data.get('is_active')
            if is_active is None:
                raise ValueError
            if str(is_active).lower() not in ['true', 'false', '1', '0']:
                raise ValueError
            is_active = str(is_active).lower() in ['true', '1']
        except ValueError:
            return Response(
                {'error': 'is_active field must be a boolean value.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        cooperativa.is_active = is_active
        cooperativa.save(update_fields=['is_active'])
        
        return Response({
            'id':             cooperativa.id,
            'name':           cooperativa.name,
            'new_is_active':  cooperativa.is_active,
        })

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[AllowAny],
        url_path='available',
    )
    def available(self, request):
        qs   = self.filter_queryset(
            self.get_queryset().filter(is_active=True)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                CooperativaSerializer(page, many=True).data
            )
        return Response(CooperativaSerializer(qs, many=True).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
    )
    def stats(self, request):
        qs      = Cooperativa.objects.all()
        active  = qs.filter(is_active=True)
        data    = active.aggregate(
            total_active   = Count('id'),
        )
        
        data['total_inactive'] = qs.filter(is_active=False).count()
        
        rutas_counts = [coop.total_rutas for coop in active]
        if rutas_counts:
            data['avg_rutas_per_coop'] = round(sum(rutas_counts) / len(rutas_counts), 2)
            data['max_rutas_in_a_coop'] = max(rutas_counts)
            data['min_rutas_in_a_coop'] = min(rutas_counts)
        else:
            data['avg_rutas_per_coop'] = 0.0
            data['max_rutas_in_a_coop'] = 0
            data['min_rutas_in_a_coop'] = 0

        return Response(data)