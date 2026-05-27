# transit/views/chofer.py
from rest_framework import viewsets
from transit.models import Chofer
from transit.serializers.chofer import ChoferSerializer
from transit.permissions import IsStaffOrReadOnly
from transit.pagination import StandardPagination

class ChoferViewSet(viewsets.ModelViewSet):
    queryset           = Chofer.objects.all()
    serializer_class   = ChoferSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filterset_fields   = ['is_active']
    search_fields      = ['first_name', 'last_name', 'license_number']