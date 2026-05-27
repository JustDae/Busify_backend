# transit/serializers/ruta.py
from rest_framework import serializers
from transit.models import Ruta


class RutaSerializer(serializers.ModelSerializer):
    total_paradas = serializers.SerializerMethodField()

    class Meta:
        model  = Ruta
        fields = [
            'id', 'name', 'description', 'origin', 'destination',
            'base_fare', 'is_active', 'total_paradas', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_total_paradas(self, obj):
        return obj.paradas.filter(is_active=True).count()

    def validate_name(self, value):
        qs = Ruta.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A route with this name already exists.')
        return value