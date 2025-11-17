# ventas/views.py

from rest_framework import viewsets
from .models import Venta, DetalleVenta, Pago
from .serializers import VentaSerializer, DetalleVentaSerializer, PagoSerializer

class VentaViewSet(viewsets.ModelViewSet):
    # Optimizamos trayendo cliente y pre-cargando los detalles
    queryset = Venta.objects.all().select_related('cliente').prefetch_related('detalles', 'pagos').order_by('-fechaVenta')
    serializer_class = VentaSerializer

class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer