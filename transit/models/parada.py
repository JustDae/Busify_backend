# transit/models/parada.py
from django.db import models
from .ruta import Ruta


class Parada(models.Model):
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    distance    = models.DecimalField(max_digits=10, decimal_places=2)
    sequence    = models.PositiveIntegerField(default=1)
    is_active   = models.BooleanField(default=True)
    ruta        = models.ForeignKey(
        Ruta,
        on_delete=models.PROTECT,
        related_name='paradas',
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return self.name

    @property
    def estimated_minutes(self):
        return round(float(self.distance) * 1.5, 2)

    @property
    def has_sequence(self):
        return self.sequence > 0