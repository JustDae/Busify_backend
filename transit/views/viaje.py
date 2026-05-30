# transit/views/viaje.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter 
from django_filters.rest_framework import DjangoFilterBackend
from transit.models import Viaje
from transit.serializers.viaje import ViajeSerializer
from transit.filters import ViajeFilter 
from transit.pagination import StandardPagination


class ViajeViewSet(viewsets.ModelViewSet):
    serializer_class   = ViajeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class   = StandardPagination
    
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = ViajeFilter 

    search_fields      = ['status', 'ruta__name', 'bus__plate', 'chofer__last_name']
    ordering_fields    = ['departure_time', 'passenger_count']
    ordering           = ['-departure_time']
    http_method_names  = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        return (
            Viaje.objects
            .select_related('ruta', 'bus', 'chofer')
            .all()
        )

    @action(detail=True, methods=['post'], url_path='add-passenger')
    def add_passenger(self, request, pk=None):
        viaje = self.get_object()
        if viaje.status not in ['scheduled', 'delayed']:
            return Response(
                {'error': f'Cannot add passengers to a trip with status "{viaje.status}".'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            quantity = int(request.data.get('quantity', 1))
            if quantity <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                {'error': 'Quantity must be a positive integer.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if viaje.passenger_count + quantity > viaje.bus.capacity:
            return Response(
                {'error': f'Insufficient capacity: only {viaje.bus.capacity - viaje.passenger_count} seats available.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        viaje.passenger_count += quantity
        viaje.save(update_fields=['passenger_count'])
        return Response(ViajeSerializer(viaje).data)

    @action(detail=True, methods=['post'], url_path='start-route')
    def start_route(self, request, pk=None):
        viaje = self.get_object()
        if viaje.status != 'scheduled':
            return Response(
                {'error': 'Only scheduled trips can be started.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        viaje.status = 'en_route'
        viaje.save(update_fields=['status'])
        return Response(ViajeSerializer(viaje).data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdminUser],
        url_path='update-status',
    )
    def update_status(self, request, pk=None):
        viaje          = self.get_object()
        new_status     = request.data.get('status')
        valid_statuses = [s[0] for s in Viaje.STATUS_CHOICES]

        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Valid options: {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        viaje.status = new_status
        viaje.save(update_fields=['status'])
        return Response(ViajeSerializer(viaje).data)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAdminUser],
        url_path='stats',
    )
    def stats(self, request):
        from django.db.models import Count, Sum
        qs     = Viaje.objects.all()
        totals = qs.aggregate(
            total_trips      = Count('id'),
            total_passengers = Sum('passenger_count'),
        )
        by_status = {
            s: qs.filter(status=s).count()
            for s, _ in Viaje.STATUS_CHOICES
        }
        return Response({
            'total_trips':      totals['total_trips'],
            'total_passengers': totals['total_passengers'] or 0,
            'by_status':        by_status,
        })