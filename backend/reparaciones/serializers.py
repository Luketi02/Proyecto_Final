# reparaciones/serializers.py

from rest_framework import serializers
from .models import Dispositivo
from usuarios.models import Usuario
from .models import Diagnostico
from .models import Reparacion
from usuarios.serializers import UsuarioSerializer


class DispositivoSerializer(serializers.ModelSerializer):
    
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
            'propietario', 
            'propietario_id' 
        ]
        read_only_fields = ['fechaIngreso']
        
class DiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        # Por ahora, exponemos todos los campos que definimos
        fields = [
            'idDiagnostico',
            'descripcionFalla',
            'fechaDiagnostico',
            'costoDiagnostico'
        ]
        read_only_fields = ['fechaDiagnostico']


class ReparacionSerializer(serializers.ModelSerializer):
    
    # --- Campos de LECTURA (GET) ---
    # Mostramos los objetos completos
    dispositivo = DispositivoSerializer(read_only=True)
    cliente = UsuarioSerializer(read_only=True)
    tecnicoAsignado = UsuarioSerializer(read_only=True)
    diagnostico = DiagnosticoSerializer(read_only=True)
    
    # --- Campos de ESCRITURA (POST/PUT) ---
    # Asignamos usando solo los IDs
    dispositivo_id = serializers.PrimaryKeyRelatedField(
        queryset=Dispositivo.objects.all(), source='dispositivo', write_only=True
    )
    cliente_id = serializers.PrimaryKeyRelatedField(
            queryset=Usuario.objects.all(),
            source='cliente',
            write_only=True,
    )
    # El técnico y el diagnóstico son opcionales al crear
    tecnicoAsignado_id = serializers.PrimaryKeyRelatedField(
             queryset=Usuario.objects.all(),
            source='tecnicoAsignado',
            write_only=True,
            required=False
    )
    diagnostico_id = serializers.PrimaryKeyRelatedField(
        queryset=Diagnostico.objects.all(), source='diagnostico', write_only=True, required=False
    )

    class Meta:
        model = Reparacion
        fields = [
            'idReparacion', 'etapa', 'fechaInicio', 'fechaEntrega', 
            'descCliente', 'codigoSec',
            
            # Campos de Lectura
            'dispositivo', 'cliente', 'tecnicoAsignado', 'diagnostico',
            
            # Campos de Escritura
            'dispositivo_id', 'cliente_id', 'tecnicoAsignado_id', 'diagnostico_id'
        ]
        read_only_fields = ['fechaInicio', 'fechaEntrega', 'codigoSec']