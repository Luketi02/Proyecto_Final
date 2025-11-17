# reparaciones/models.py

from django.db import models
from usuarios.models import Usuario # Importa el Usuario

class Dispositivo(models.Model):
    idDispositivo = models.AutoField(primary_key=True)

    propietario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='dispositivos' # 'related_name' es una buena práctica
    )

    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numeroSerie = models.CharField(max_length=100, null=True, blank=True)
    fechaIngreso = models.DateTimeField(auto_now_add=True)
    imagen = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} (Dueño: {self.propietario.nombre})"