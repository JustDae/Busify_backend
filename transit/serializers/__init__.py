# transit/serializers/__init__.py
from .auth import CustomTokenSerializer
from .ruta import RutaSerializer
from .parada import ParadaSerializer, ParadaSummarySerializer
from .bus import BusSerializer, MaintenanceRecordSerializer
from .chofer import ChoferSerializer
from .viaje import ViajeSerializer
from .user import UserSerializer, RegisterSerializer