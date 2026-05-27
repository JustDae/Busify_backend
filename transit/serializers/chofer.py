# transit/serializers/chofer.py
from rest_framework import serializers
from transit.models import Chofer


class ChoferSerializer(serializers.ModelSerializer):
    full_name        = serializers.SerializerMethodField()
    rate_with_bonus  = serializers.SerializerMethodField()
    is_experienced   = serializers.SerializerMethodField()

    class Meta:
        model  = Chofer
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'license_number',
            'daily_rate', 'rate_with_bonus', 'trips_completed', 
            'is_experienced', 'is_active', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_full_name(self, obj):
        return obj.full_name

    def get_rate_with_bonus(self, obj):
        return obj.rate_with_bonus

    def get_is_experienced(self, obj):
        return obj.is_experienced