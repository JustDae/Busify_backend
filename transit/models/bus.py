# transit/models/bus.py
from django.db import models

class Bus(models.Model):
    STATUS_CHOICES = [
        ('active',        'Activo'),
        ('maintenance',   'Mantenimiento'),
        ('inactive',      'Inactivo'),
    ]

    unit_number = models.CharField(max_length=10, unique=True)
    plate       = models.CharField(max_length=10, unique=True)
    model       = models.CharField(max_length=50)
    capacity    = models.PositiveIntegerField()
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Bus #{self.unit_number} — {self.plate} ({self.status})'

    def calculate_total_spent(self):
        self.total_spent = sum(
            record.cost 
            for record in self.maintenance_records.all()
        )
        self.save(update_fields=['total_spent'])


class MaintenanceRecord(models.Model):
    bus         = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='maintenance_records')
    description = models.CharField(max_length=255)
    cost        = models.DecimalField(max_digits=10, decimal_places=2)
    created_at  = models.DateTimeField(auto_now_add=True)

    @property
    def cost_with_tax(self):
        return float(self.cost) * 1.15 

    def __str__(self):
        return f'Record for Bus {self.bus.unit_number} — {self.description}'