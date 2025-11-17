# reparaciones/models.py

from django.db import models
from django.utils import timezone  # Lo necesitamos para el campo de fecha
from usuarios.models import Usuario  # Importamos Usuario (para Dispositivo y Reparacion)



class Dispositivo(models.Model):
    idDispositivo = models.AutoField(primary_key=True)
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='dispositivos')
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numeroSerie = models.CharField(max_length=100, null=True, blank=True)
    fechaIngreso = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='dispositivos/', null=True, blank=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} (Dueño: {self.propietario.nombre})"


class Diagnostico(models.Model):
    idDiagnostico = models.AutoField(primary_key=True)
    descripcionFalla = models.TextField()
    fechaDiagnostico = models.DateTimeField(auto_now_add=True)
    costoDiagnostico = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # idVenta y insumosUtilizados (los vemos después)
    
    def __str__(self):
        return f"Diagnóstico #{self.idDiagnostico} - Costo: ${self.costoDiagnostico}"

class Reparacion(models.Model):
    
    # --- Definimos los ESTADOS (Etapas) ---
    ESTADO_ESPERANDO_DIAGNOSTICO = 'Esperando Diagnostico'
    ESTADO_ESPERANDO_RESPUESTA = 'Esperando Respuesta del Cliente'
    ESTADO_ESPERANDO_INSUMOS = 'Esperando Insumos'
    ESTADO_EN_REPARACION = 'En Reparacion'
    ESTADO_LISTO_PARA_RETIRAR = 'Listo para Retirar'
    ESTADO_RETIRADO = 'Retirado'
    ESTADO_RECHAZADO = 'Rechazado por el cliente'

    ESTADO_CHOICES = [
        (ESTADO_ESPERANDO_DIAGNOSTICO, 'Esperando Diagnóstico'),
        (ESTADO_ESPERANDO_RESPUESTA, 'Esperando Respuesta del Cliente'),
        (ESTADO_ESPERANDO_INSUMOS, 'Esperando Insumos'),
        (ESTADO_EN_REPARACION, 'En Reparación'),
        (ESTADO_LISTO_PARA_RETIRAR, 'Listo para Retirar'),
        (ESTADO_RETIRADO, 'Retirado'),
        (ESTADO_RECHAZADO, 'Rechazado por el cliente'),
    ]

    idReparacion = models.AutoField(primary_key=True)
    
    # --- Relaciones Clave ---
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='reparaciones')
    cliente = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='reparaciones')
    tecnicoAsignado = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='reparaciones_asignadas')
    diagnostico = models.OneToOneField(Diagnostico, on_delete=models.SET_NULL, null=True, blank=True)
    
    # --- Campos de tu doc ---
    fechaInicio = models.DateTimeField(default=timezone.now) # Usamos timezone.now
    fechaEntrega = models.DateTimeField(null=True, blank=True)
    etapa = models.CharField(max_length=100, choices=ESTADO_CHOICES, default=ESTADO_ESPERANDO_DIAGNOSTICO)
    descCliente = models.TextField(blank=True, null=True)
    codigoSec = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return f"Reparación #{self.idReparacion} - {self.dispositivo.marca} - {self.etapa}"