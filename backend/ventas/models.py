# ventas/models.py

from django.db import models
from django.utils import timezone
from usuarios.models import Usuario  # El Cliente
from stock.models import Producto    # Lo que vendemos

# 1. LA VENTA (La Cabecera)
class Venta(models.Model):
    idVenta = models.AutoField(primary_key=True)
    
    # Cliente que compra (puede ser nulo si es consumidor final anónimo, 
    # aunque tu doc dice que se vincula a usuario [cite: 1673])
    cliente = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='compras')
    
    fechaVenta = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Código de seguridad para retiro [cite: 1675]
    codigoSec = models.CharField(max_length=10, blank=True, null=True)
    
    # Estado de la venta (Pendiente, Completada, Cancelada)
    ESTADOS_VENTA = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS_VENTA, default='PENDIENTE')

    def __str__(self):
        return f"Venta #{self.idVenta} - {self.cliente} - ${self.total}"

# 2. DETALLE DE VENTA (Los renglones de la factura)
# Relaciona la Venta con los Productos
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    
    cantidad = models.IntegerField(default=1)
    precioUnitario = models.DecimalField(max_digits=10, decimal_places=2) # Precio al momento de la venta
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calculamos el subtotal automáticamente antes de guardar
        self.subtotal = self.cantidad * self.precioUnitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en Venta #{self.venta.idVenta}"

# 3. EL PAGO
class Pago(models.Model):
    MEDIOS_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('DEBITO', 'Tarjeta de Débito'),
        ('CREDITO', 'Tarjeta de Crédito'),
        ('QR', 'QR / Billetera Virtual'),
    ]

    idPago = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='pagos')
    
    fechaPago = models.DateTimeField(default=timezone.now)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    medioPago = models.CharField(max_length=50, choices=MEDIOS_PAGO)
    
    # Comprobante o nota (ej: número de operación de transferencia)
    comprobante = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Pago #{self.idPago} - {self.medioPago}: ${self.monto}"

