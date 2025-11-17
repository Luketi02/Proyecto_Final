# stock/serializers.py

from rest_framework import serializers
from .models import Proveedor, Producto, Stock
from .models import OrdenCompra, DetalleOrden

# 1. SERIALIZADOR DE PROVEEDOR
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = [
            'idProveedor', 
            'nombreProveedor', 
            'correo', 
            'telefono', 
            'direccion', 
            'estado'
        ]

# 2. SERIALIZADOR DE PRODUCTO
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'idProducto', 
            'nombre', 
            'descripcion', 
            'precioVenta', 
            'categoria', 
            'estado', 
            'imagen'
        ]

# 3. SERIALIZADOR DE STOCK
class StockSerializer(serializers.ModelSerializer):
    
    # --- LECTURA (GET) ---
    # Muestra todos los detalles del producto (nombre, precio, etc.)
    producto = ProductoSerializer(read_only=True)

    # --- ESCRITURA (POST/PUT) ---
    # Permite asignar el producto usando solo su ID
    # (Sin el 'pk_field' que nos dio problemas antes, dejamos que Django use el default)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(), 
        source='producto', 
        write_only=True
    )

    class Meta:
        model = Stock
        fields = [
            'idStock', 
            'cantDisponible', 
            'stockMinimo', 
            'producto',     # Objeto completo (para ver)
            'producto_id'   # ID (para guardar)
        ]
 
 #4. SERIALIZADOR DE ORDENES DE COMPRA 
        
class DetalleOrdenSerializer(serializers.ModelSerializer):
    # Lectura
    producto_data = ProductoSerializer(source='producto', read_only=True)
    
    # Escritura
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(), source='producto', write_only=True
    )

    class Meta:
        model = DetalleOrden
        fields = ['id', 'orden', 'producto_data', 'producto_id', 'cantidad', 'costoUnitario']


class OrdenCompraSerializer(serializers.ModelSerializer):
    # Lectura
    proveedor_data = ProveedorSerializer(source='proveedor', read_only=True)
    detalles = DetalleOrdenSerializer(many=True, read_only=True)
    
    # Escritura
    proveedor_id = serializers.PrimaryKeyRelatedField(
        queryset=Proveedor.objects.all(), source='proveedor', write_only=True
    )

    class Meta:
        model = OrdenCompra
        fields = [
            'idOrden', 'fechaEmision', 'estado', 'solTec', 'comentarios', 'presupuestoAdjunto',
            'proveedor_data', 'proveedor_id', 
            'detalles'
        ]