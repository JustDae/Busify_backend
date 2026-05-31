from rest_framework import serializers
from transit.models import Cooperativa


class CooperativaSerializer(serializers.ModelSerializer):
    total_rutas = serializers.SerializerMethodField()

    class Meta:
        model  = Cooperativa
        fields = [
            'id', 'name', 'is_active', 'total_rutas', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_total_rutas(self, obj):
        return obj.rutas.filter(is_active=True).count()

    def validate_name(self, value):
        qs = Cooperativa.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A cooperative with this name already exists.')
        return value