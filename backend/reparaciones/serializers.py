# reparaciones/serializers.py

from rest_framework import serializers
from .models import Dispositivo
from usuarios.models import Usuario

# ---
# ¡¡¡ OJO !!!
# NO ESTAMOS IMPORTANDO UsuarioSerializer
# ---

class DispositivoSerializer(serializers.ModelSerializer):
    
    # ---
    # ¡AQUÍ ESTÁ EL CAMBIO DE DIAGNÓSTICO!
    # ---
    # En lugar de usar el 'UsuarioSerializer', usamos un campo de texto
    # que automáticamente llamará al método '__str__' de tu modelo Usuario
    # (El que definiste como: f"{self.nombre} {self.apellido} ({self.email})")
    propietario = serializers.StringRelatedField(read_only=True)

    # (El campo para escribir/POST sigue igual)
    propietario_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(), 
        source='propietario',
        write_only=True,
    )

    class Meta:
        model = Dispositivo
        fields = [
            'idDispositivo',
            'marca',
            'modelo',
            'numeroSerie',
            'fechaIngreso',
            'imagen',
            'propietario',  # <-- Este campo ahora es un StringRelatedField
            'propietario_id' 
        ]
        read_only_fields = ['fechaIngreso']