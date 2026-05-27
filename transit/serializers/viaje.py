# transit/serializers/viaje.py
from rest_framework import serializers
from transit.models import Viaje
from transit.serializers.ruta import RutaSerializer
from transit.serializers.chofer import ChoferSerializer


class ViajeSerializer(serializers.ModelSerializer):
    ruta            = RutaSerializer(read_only=True)
    chofer          = ChoferSerializer(read_only=True)
    bus_plate       = serializers.CharField(source='bus.plate', read_only=True)
    available_seats = serializers.SerializerMethodField()
    is_full         = serializers.SerializerMethodField()

    class Meta:
        model  = Viaje
        fields = [
            'id', 'status', 'passenger_count', 'available_seats', 'is_full',
            'departure_time', 'estimated_arrival', 'ruta', 'chofer', 'bus_plate',
        ]

    def get_available_seats(self, obj):
        return obj.available_seats

    def get_is_full(self, obj):
        return obj.is_full