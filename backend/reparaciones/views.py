# reparaciones/views.py

from rest_framework import viewsets
from .models import Dispositivo, Diagnostico, Reparacion
from .serializers import DispositivoSerializer, DiagnosticoSerializer, ReparacionSerializer

#Vista de Dispositivo

class DispositivoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver o editar Dispositivos.
    """
    queryset = Dispositivo.objects.all().select_related('propietario').order_by('marca')
    serializer_class = DispositivoSerializer
    
#Vista de Diagnostico

class DiagnosticoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver o editar Diagnósticos.
    """
    queryset = Diagnostico.objects.all()
    serializer_class = DiagnosticoSerializer
    
# Vista de Reparación 

class ReparacionViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver o editar Reparaciones.
    """
    # Optimizamos la consulta para traer todas las relaciones
    queryset = Reparacion.objects.all().select_related(
        'dispositivo', 'cliente', 'tecnicoAsignado', 'diagnostico'
    ).order_by('-fechaInicio')
    serializer_class = ReparacionSerializer
    
