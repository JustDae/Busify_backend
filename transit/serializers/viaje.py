# transit/serializers/viaje.py
from rest_framework import serializers
from transit.models import Bus, Chofer, Ruta, Viaje
from transit.serializers.ruta import RutaSerializer
from transit.serializers.chofer import ChoferSerializer


class ViajeSerializer(serializers.ModelSerializer):
    ruta            = RutaSerializer(read_only=True)
    chofer          = ChoferSerializer(read_only=True)
    bus             = serializers.PrimaryKeyRelatedField(read_only=True)
    bus_plate       = serializers.CharField(source='bus.plate', read_only=True)
    available_seats = serializers.SerializerMethodField()
    is_full         = serializers.SerializerMethodField()

    class Meta:
        model  = Viaje
        fields = [
            'id', 'status', 'passenger_count', 'available_seats', 'is_full',
            'departure_time', 'estimated_arrival', 'ruta', 'chofer', 'bus', 'bus_plate',
        ]

    def to_internal_value(self, data):
        attrs = super().to_internal_value(data)
        related_fields = {
            'ruta': Ruta.objects.filter(is_active=True),
            'bus': Bus.objects.filter(status='active'),
            'chofer': Chofer.objects.filter(is_active=True),
        }

        for field_name, queryset in related_fields.items():
            if field_name in data:
                try:
                    attrs[field_name] = queryset.get(pk=data[field_name])
                except (TypeError, ValueError):
                    raise serializers.ValidationError({
                        field_name: 'Invalid ID.'
                    })
                except queryset.model.DoesNotExist:
                    raise serializers.ValidationError({
                        field_name: 'Object not found or unavailable.'
                    })

        return attrs

    def get_available_seats(self, obj):
        return obj.available_seats

    def get_is_full(self, obj):
        return obj.is_full
