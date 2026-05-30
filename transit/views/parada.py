# transit/views/parada.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Max, Min, Sum, Count 
from transit.models import Parada
from transit.serializers.parada import ParadaSerializer, ParadaSummarySerializer
from transit.permissions import IsStaffOrReadOnly
from transit.pagination import StandardPagination

class ParadaViewSet(viewsets.ModelViewSet):

    queryset           = Parada.objects.select_related('ruta').all()
    serializer_class   = ParadaSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ['is_active', 'ruta']
    
    search_fields      = ['name', 'description', 'ruta__name']
    ordering_fields    = ['name', 'distance', 'sequence', 'created_at']
    ordering           = ['name']

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdminUser],
        url_path='update-sequence', 
    )
    def update_sequence(self, request, pk=None):
        parada = self.get_object()
        try:
            sequence = int(request.data.get('sequence', 0))
            if sequence <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                {'error': 'Sequence must be a positive integer.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        parada.sequence = sequence
        parada.save(update_fields=['sequence'])
        
        return Response({
            'id':           parada.id,
            'name':         parada.name,
            'new_sequence': parada.sequence,
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
                ParadaSummarySerializer(page, many=True).data
            )
        return Response(ParadaSummarySerializer(qs, many=True).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
    )
    def stats(self, request):
        qs      = Parada.objects.all()
        active  = qs.filter(is_active=True)
        data    = active.aggregate(
            total_active   = Count('id'),
            avg_distance   = Avg('distance'),
            max_distance   = Max('distance'),
            min_distance   = Min('distance'),
            total_distance = Sum('distance'), 
        )
        
        data['total_inactive'] = qs.filter(is_active=False).count()
        data['no_sequence']    = active.filter(sequence=0).count() 
        
        if data['avg_distance']:
            data['avg_distance'] = round(float(data['avg_distance']), 2)
            
        return Response(data)