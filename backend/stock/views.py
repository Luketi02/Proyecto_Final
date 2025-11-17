# stock/views.py

from rest_framework import viewsets
from .models import Proveedor, Producto, Stock
from .serializers import ProveedorSerializer, ProductoSerializer, StockSerializer
from .models import OrdenCompra, DetalleOrden
from .serializers import OrdenCompraSerializer, DetalleOrdenSerializer

# 1. Vista de Proveedores
class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all().order_by('nombreProveedor')
    serializer_class = ProveedorSerializer

# 2. Vista de Productos
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('nombre')
    serializer_class = ProductoSerializer

# 3. Vista de Stock
class StockViewSet(viewsets.ModelViewSet):
    # Usamos select_related para traer el Producto asociado de una sola vez
    queryset = Stock.objects.all().select_related('producto')
    serializer_class = StockSerializer
    
#4. Vista de Orden de Compra
class OrdenCompraViewSet(viewsets.ModelViewSet):
    queryset = OrdenCompra.objects.all().select_related('proveedor').prefetch_related('detalles')
    serializer_class = OrdenCompraSerializer

#5. Vista de Detalle de Orden de Compra
class DetalleOrdenViewSet(viewsets.ModelViewSet):
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer