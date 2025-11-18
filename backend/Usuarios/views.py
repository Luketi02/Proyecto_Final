from rest_framework import viewsets
from .models import Rol, Usuario
from .serializers import RolSerializer, UsuarioSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import Usuario, Rol
import random
from rest_framework.permissions import AllowAny

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
    
GOOGLE_CLIENT_ID = "104545876188-2ej069cpkekctc64unc737rrvl4fb4u6.apps.googleusercontent.com"

class GoogleLoginView(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response({'error': 'No se proveyó token'}, status=400)

        try:
            # 1. Verificar el token con Google
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            
            # 2. Obtener el email del usuario de Google
            email = idinfo['email']
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')

            # 3. Buscar si el usuario ya existe en IFixNet
            try:
                user = Usuario.objects.get(email=email)
            except Usuario.DoesNotExist:
                # 4. Si no existe, lo creamos automáticamente
                # Asignamos un rol por defecto (ej: Cliente, ID 3)
                # ¡Asegurate de tener un Rol con ID 3 o cambiá este número!
                rol_cliente, _ = Rol.objects.get_or_create(idRol=3, defaults={'nombreRol': 'Cliente'})
                
                user = Usuario.objects.create(
                    email=email,
                    nombre=first_name,
                    apellido=last_name,
                    rol=rol_cliente,
                    # Generamos una contraseña aleatoria porque entra con Google
                    password=f"google_{random.randint(10000,99999)}" 
                )
                user.set_unusable_password() # Para que no pueda entrar con contraseña normal
                user.save()

            # 5. Generar los tokens JWT de nuestro sistema
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'email': user.email,
                    'nombre': user.nombre,
                    'rol': user.rol.nombreRol if user.rol else None
                }
            })

        except ValueError:
            return Response({'error': 'Token de Google inválido'}, status=400)