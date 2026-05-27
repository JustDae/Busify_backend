# transit/models/viaje.py
from django.db import models
from .ruta import Ruta
from .bus import Bus
from .chofer import Chofer


class Viaje(models.Model):
    STATUS_CHOICES = [
        ('programado', 'Programado'),
        ('en_ruta',    'En Ruta'),
        ('completado', 'Completado'),
        ('retrasado',  'Retrasado'),
        ('cancelado',  'Cancelado'),
    ]

    status            = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    passenger_count   = models.PositiveIntegerField(default=0)
    departure_time    = models.DateTimeField()
    estimated_arrival = models.DateTimeField()
    ruta              = models.ForeignKey(
        Ruta,
        on_delete=models.PROTECT,
        related_name='viajes',
    )
    bus               = models.ForeignKey(
        Bus,
        on_delete=models.PROTECT,
        related_name='viajes',
    )
    chofer            = models.ForeignKey(
        Chofer,
        on_delete=models.PROTECT,
        related_name='viajes',
    )
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-departure_time']

    def __str__(self):
        return f'Viaje #{self.id} — Route: {self.ruta.name} ({self.status})'

    @property
    def available_seats(self):
        return max(0, self.bus.capacity - self.passenger_count)

    @property
    def is_full(self):
        return self.passenger_count >= self.bus.capacity