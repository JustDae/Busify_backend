from django.contrib import admin

# Register your models here.
# transit/admin.py
from django.contrib import admin
from transit.models import Ruta, Parada, Chofer, Bus, MaintenanceRecord, Viaje


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name', 'origin', 'destination', 'base_fare', 'is_active', 'created_at']
    list_filter   = ['is_active']
    search_fields = ['name', 'origin', 'destination']


@admin.register(Parada)
class ParadaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name', 'sequence', 'distance', 'is_active', 'ruta']
    list_filter   = ['is_active', 'ruta']
    search_fields = ['name', 'description']
    list_editable = ['sequence', 'distance', 'is_active']


@admin.register(Chofer)
class ChoferAdmin(admin.ModelAdmin):
    list_display  = ['id', 'first_name', 'last_name', 'license_number', 'daily_rate', 'is_active']
    list_filter   = ['is_active']
    search_fields = ['first_name', 'last_name', 'license_number']
    list_editable = ['daily_rate', 'is_active']


class MaintenanceRecordInline(admin.TabularInline):
    model  = MaintenanceRecord
    extra  = 0
    fields = ['description', 'cost']


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display    = ['id', 'unit_number', 'plate', 'model', 'status', 'total_spent', 'created_at']
    list_filter     = ['status']
    search_fields   = ['unit_number', 'plate']
    inlines         = [MaintenanceRecordInline]
    readonly_fields = ['total_spent', 'created_at', 'updated_at']


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display    = ['id', 'ruta', 'bus', 'chofer', 'status', 'departure_time', 'created_at']
    list_filter     = ['status', 'ruta']
    search_fields   = ['bus__plate', 'chofer__last_name', 'ruta__name']
    readonly_fields = ['created_at', 'updated_at']