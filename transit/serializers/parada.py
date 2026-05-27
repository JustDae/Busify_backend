# transit/serializers/parada.py
from rest_framework import serializers
from transit.models import Parada
from transit.serializers.ruta import RutaSerializer


class ParadaSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model  = Parada
        fields = ['id', 'name', 'distance', 'sequence', 'is_active']


class ParadaSerializer(serializers.ModelSerializer):
    ruta              = RutaSerializer(read_only=True)
    ruta_id           = serializers.PrimaryKeyRelatedField(
        source='ruta',
        write_only=True,
        queryset=Parada.objects.none(),
    )
    estimated_minutes = serializers.SerializerMethodField()
    has_sequence      = serializers.SerializerMethodField()

    class Meta:
        model  = Parada
        fields = [
            'id', 'name', 'description',
            'distance', 'estimated_minutes',
            'sequence', 'has_sequence', 'is_active',
            'ruta', 'ruta_id',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from transit.models import Ruta
        self.fields['ruta_id'].queryset = Ruta.objects.filter(is_active=True)

    def get_estimated_minutes(self, obj):
        return obj.estimated_minutes

    def get_has_sequence(self, obj):
        return obj.has_sequence

    def validate_distance(self, value):
        if value <= 0:
            raise serializers.ValidationError('Distance must be greater than 0 km.')
        return value

    def validate_sequence(self, value):
        if value < 0:
            raise serializers.ValidationError('Sequence cannot be negative.')
        return value