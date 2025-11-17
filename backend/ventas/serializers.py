# ventas/serializers.py

from rest_framework import serializers
from .models import Venta, DetalleVenta, Pago
from usuarios.models import Usuario
from stock.models import Producto

# Importamos los serializadores de las otras apps para mostrar detalles lindos
from usuarios.serializers import UsuarioSerializer
from stock.serializers import ProductoSerializer

# 1. SERIALIZADOR DE PAGO
class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['idPago', 'venta', 'fechaPago', 'monto', 'medioPago', 'comprobante']


# 2. SERIALIZADOR DE DETALLE (El renglón de la factura)
class DetalleVentaSerializer(serializers.ModelSerializer):
    # Lectura: Mostramos el producto completo
    producto = ProductoSerializer(read_only=True)
    
    # Escritura: Asignamos por ID
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(), 
        source='producto', 
        write_only=True
    )

    class Meta:
        model = DetalleVenta
        fields = [
            'id', 
            'venta', 
            'producto', 
            'producto_id', 
            'cantidad', 
            'precioUnitario', 
            'subtotal'
        ]


# 3. SERIALIZADOR DE VENTA (La Cabecera)
class VentaSerializer(serializers.ModelSerializer):
    
    # --- LECTURA ---
    # Mostramos al cliente completo
    cliente = UsuarioSerializer(read_only=True)
    
    # ¡MAGIA! Mostramos los detalles y pagos anidados automáticamente
    # 'detalles' y 'pagos' son los 'related_name' que definimos en models.py
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    pagos = PagoSerializer(many=True, read_only=True)

    # --- ESCRITURA ---
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(), 
        source='cliente', 
        write_only=True,
        required=False,
        allow_null=True # Porque puede ser un consumidor final anónimo
    )

    class Meta:
        model = Venta
        fields = [
            'idVenta', 
            'fechaVenta', 
            'total', 
            'estado', 
            'codigoSec',
            'cliente',      # Objeto completo
            'cliente_id',   # Solo ID
            'detalles',     # Lista de productos comprados (Solo lectura por ahora)
            'pagos'         # Lista de pagos realizados (Solo lectura por ahora)
        ]