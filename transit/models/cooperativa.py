from django.db import models

class Cooperativa(models.Model):
    name        = models.CharField(max_length=200, unique=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Cooperativa"
        verbose_name_plural = "Cooperativas"

    def __str__(self):
        return self.name

    @property
    def total_rutas(self):
        return self.rutas.count()