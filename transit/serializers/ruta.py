from rest_framework import serializers
from transit.models import Ruta, Viaje


class RutaSerializer(serializers.ModelSerializer):
    total_paradas = serializers.SerializerMethodField()
    cooperativa_name = serializers.ReadOnlyField(source='cooperativa.name')
    
    tarifa = serializers.DecimalField(source='base_fare', max_digits=10, decimal_places=2, read_only=True)
    total_buses = serializers.SerializerMethodField()
    has_buses_activos = serializers.SerializerMethodField()

    class Meta:
        model  = Ruta
        fields = [
            'id', 'cooperativa', 'cooperativa_name', 'name', 'description', 
            'origin', 'destination', 'base_fare', 'tarifa', 'is_active', 
            'total_paradas', 'total_buses', 'has_buses_activos', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_total_paradas(self, obj):
        return obj.paradas.filter(is_active=True).count()

    def get_total_buses(self, obj):
        return Viaje.objects.filter(ruta=obj).count()

    def get_has_buses_activos(self, obj):
        return Viaje.objects.filter(ruta=obj, status__iexact='En Ruta').exists()

    def validate_name(self, value):
        qs = Ruta.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A route with this name already exists.')
        return value