# stock/models.py

from django.db import models

# 1. PROVEEDOR [cite: 1692]
class Proveedor(models.Model):
    idProveedor = models.AutoField(primary_key=True)
    nombreProveedor = models.CharField(max_length=150)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    # Estado: Activo si aceptó orden en el último año (lógica futura)
    estado = models.BooleanField(default=True) 

    def __str__(self):
        return self.nombreProveedor

# 2. PRODUCTO [cite: 1667]
class Producto(models.Model):
    CATEGORIAS = [
        ('REPUESTO', 'Repuesto'),
        ('ACCESORIO', 'Accesorio'),
        ('PERIFERICO', 'Periférico'),
        ('INSUMO', 'Insumo Taller'),
    ]

    idProducto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precioVenta = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    # Estado: Activo, discontinuado, etc.
    estado = models.BooleanField(default=True) 
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} (${self.precioVenta})"

# 3. STOCK [cite: 1670]
class Stock(models.Model):
    idStock = models.AutoField(primary_key=True)
    
    # Relación 1 a 1: Cada producto tiene UN registro de stock
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='stock')
    
    cantDisponible = models.IntegerField(default=0)
    stockMinimo = models.IntegerField(default=5) # Umbral de alerta

    def __str__(self):
        return f"Stock de {self.producto.nombre}: {self.cantDisponible}"

# 4. ORDEN DE COMPRA (La Cabecera)
class OrdenCompra(models.Model):
    ESTADOS_ORDEN = [
        ('PENDIENTE', 'Pendiente'), # Creada por técnico o admin, aún no enviada
        ('ENVIADO', 'Enviado'),     # Enviada al proveedor
        ('ACEPTADO', 'Aceptado'),   # Proveedor aceptó
        ('RECHAZADO', 'Rechazado'), # Proveedor rechazó
        ('RECIBIDO', 'Recibido'),   # Mercadería ingresó al stock
        ('CANCELADO', 'Cancelado'),
    ]

    idOrden = models.AutoField(primary_key=True)
    
    # Una orden va dirigida a un proveedor principal (o puede ser varios, según tu lógica, 
    # pero lo estándar es una orden por proveedor. Aquí lo simplificamos a uno por orden).
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, related_name='ordenes')
    fechaEmision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_ORDEN, default='PENDIENTE')
    # "solTec": Si fue solicitada por un técnico (limita edición) - Doc Pág 96
    solTec = models.BooleanField(default=False) 
    # Comentarios o presupuesto adjunto (URL o texto)
    comentarios = models.TextField(blank=True, null=True)
    presupuestoAdjunto = models.FileField(upload_to='presupuestos/', blank=True, null=True)

    def __str__(self):
        return f"Orden #{self.idOrden} - {self.proveedor} ({self.estado})"


# 5. DETALLE DE ORDEN (Los renglones de la orden)
class DetalleOrden(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    
    cantidad = models.IntegerField(default=1)
    # Precio costo esperado (opcional, para control)
    costoUnitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en Orden #{self.orden.idOrden}"