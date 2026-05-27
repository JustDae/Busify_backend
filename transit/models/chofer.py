# transit/models/chofer.py
from django.db import models


class Chofer(models.Model):
    first_name      = models.CharField(max_length=100)
    last_name       = models.CharField(max_length=100)
    license_number  = models.CharField(max_length=50, unique=True)
    daily_rate      = models.DecimalField(max_digits=10, decimal_places=2)
    trips_completed = models.PositiveIntegerField(default=0)
    is_active       = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def rate_with_bonus(self):
        return round(float(self.daily_rate) * 1.15, 2)

    @property
    def is_experienced(self):
        return self.trips_completed > 0