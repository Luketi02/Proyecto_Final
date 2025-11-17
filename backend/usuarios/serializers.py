from rest_framework import serializers
from .models import Usuario, Rol

# --- Serializador de Rol  ---
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['idRol', 'nombreRol', 'descripcion']

# ---  Serializador de Usuario ---
class UsuarioSerializer(serializers.ModelSerializer):
    
    rol = RolSerializer(read_only=True)
    
    rol_id = serializers.PrimaryKeyRelatedField(
        queryset=Rol.objects.all(), source='rol', write_only=True
    )

    class Meta:
        model = Usuario
        
        fields = [
            'idUsuario', 'email', 'nombre', 'apellido', 'telefono', 
            'telefonoAlt', 'fotoPerfil', 'rol', 'rol_id', 'fechaRegistro',
            'notiC', 'notiW', 'modoOscuro',
            'password' 
        ]
        
        read_only_fields = ['fechaRegistro']
        
        extra_kwargs = {
            'password': {
                'write_only': True, 
                'style': {'input_type': 'password'}
            }
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        usuario = super().update(instance, validated_data)

        if password:
            usuario.set_password(password)
            usuario.save()

        return usuario