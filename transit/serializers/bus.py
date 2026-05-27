# transit/serializers/bus.py
from rest_framework import serializers
from transit.models import Bus, MaintenanceRecord
from decimal import Decimal

class MaintenanceRecordSerializer(serializers.ModelSerializer):
    cost_with_tax = serializers.SerializerMethodField()

    class Meta:
        model  = MaintenanceRecord
        fields = ['id', 'description', 'cost', 'cost_with_tax', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_cost_with_tax(self, obj):
        return obj.cost_with_tax


class BusSerializer(serializers.ModelSerializer):
    maintenance_records = MaintenanceRecordSerializer(many=True, read_only=True)
    num_records         = serializers.SerializerMethodField()

    class Meta:
        model  = Bus
        fields = [
            'id', 'unit_number', 'plate', 'model', 'capacity', 
            'status', 'total_spent', 'num_records', 'maintenance_records', 
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'total_spent', 'created_at', 'updated_at']

    def get_num_records(self, obj):
        return obj.maintenance_records.count()


class AddMaintenanceRecordSerializer(serializers.Serializer):
    bus_id      = serializers.IntegerField()
    cost        = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    description = serializers.CharField(max_length=255)

    def validate_bus_id(self, value):
        try:
            Bus.objects.get(pk=value, status='active')
        except Bus.DoesNotExist:
            raise serializers.ValidationError(
                f'Bus with ID {value} not found or is not currently active.'
            )
        return value