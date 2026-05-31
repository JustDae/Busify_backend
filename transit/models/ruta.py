from django.db import models
from transit.models.cooperativa import Cooperativa


class Ruta(models.Model):
    cooperativa = models.ForeignKey(
        Cooperativa,
        on_delete=models.SET_NULL,
        related_name='rutas',
        null=True,
        blank=True
    )
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    origin      = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    base_fare   = models.DecimalField(max_digits=10, decimal_places=2)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.origin} ➡️ {self.destination})'

    @property
    def fare_with_tax(self):
        return round(float(self.base_fare) * 1.15, 2)

    @property
    def has_description(self):
        return len(self.description) > 0