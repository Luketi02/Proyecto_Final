# ventas/admin.py
from django.contrib import admin
from .models import Venta, DetalleVenta, Pago

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0 # Para ver los productos vendidos dentro de la venta

class VentaAdmin(admin.ModelAdmin):
    list_display = ('idVenta', 'cliente', 'fechaVenta', 'total', 'estado')
    list_filter = ('estado', 'fechaVenta')
    inlines = [DetalleVentaInline] 

admin.site.register(Venta, VentaAdmin)
admin.site.register(Pago)