# reparaciones/views.py

from rest_framework import viewsets
from .models import Dispositivo
from .serializers import DispositivoSerializer # Importa el que acabamos de crear

class DispositivoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver o editar Dispositivos.
    """
    queryset = Dispositivo.objects.all().select_related('propietario').order_by('marca')
    serializer_class = DispositivoSerializer