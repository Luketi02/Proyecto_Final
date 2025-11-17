# reparaciones/admin.py
from django.contrib import admin
from .models import Dispositivo, Diagnostico, Reparacion

class ReparacionAdmin(admin.ModelAdmin):
    # Mostramos columnas útiles en la lista
    list_display = ('idReparacion', 'dispositivo', 'etapa', 'fechaInicio', 'tecnicoAsignado')
    # Filtros laterales para buscar rápido
    list_filter = ('etapa', 'fechaInicio')
    # Barra de búsqueda
    search_fields = ('dispositivo__marca', 'dispositivo__modelo', 'cliente__email')

# Registramos los modelos
admin.site.register(Dispositivo)
admin.site.register(Diagnostico)
admin.site.register(Reparacion, ReparacionAdmin)