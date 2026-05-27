# transit/views/bus.py
from rest_framework import viewsets
from transit.models import Bus
from transit.serializers.bus import BusSerializer
from transit.permissions import IsStaffOrReadOnly
from transit.pagination import StandardPagination

class BusViewSet(viewsets.ModelViewSet):
    queryset           = Bus.objects.all()
    serializer_class   = BusSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filterset_fields   = ['status']
    search_fields      = ['unit_number', 'plate', 'model']