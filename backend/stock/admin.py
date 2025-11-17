# stock/admin.py
from django.contrib import admin
from .models import Proveedor, Producto, Stock, OrdenCompra, DetalleOrden

class StockAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantDisponible', 'stockMinimo')

class DetalleOrdenInline(admin.TabularInline):
    model = DetalleOrden
    extra = 1

class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ('idOrden', 'proveedor', 'fechaEmision', 'estado')
    list_filter = ('estado', 'fechaEmision')
    inlines = [DetalleOrdenInline] # Permite cargar productos dentro de la misma orden

admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Stock, StockAdmin)
admin.site.register(OrdenCompra, OrdenCompraAdmin)
# DetalleOrden no hace falta registrarlo solo, ya se ve dentro de OrdenCompra