from rest_framework import viewsets
from .models import Rol, Usuario
from .serializers import RolSerializer, UsuarioSerializer

class RolViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar los roles de usuario.
    """
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    
    # --- Vista de Usuario ---
class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar usuarios.
    """
    # Usamos '.select_related('rol')' para optimizar la consulta
    # y traer el rol en el mismo viaje a la base de datos.
    queryset = Usuario.objects.all().select_related('rol').order_by('nombre')
    serializer_class = UsuarioSerializer
    # NOTA: Más adelante, aquí agregaremos los permisos.