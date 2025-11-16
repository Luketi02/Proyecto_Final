from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# -------------------------------
# GESTOR PERSONALIZADO DE USUARIO
# -------------------------------
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, contraseña=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")
        email = self.normalize_email(email)
        usuario = self.model(email=email, nombre=nombre, apellido=apellido, **extra_fields)
        usuario.set_password(contraseña)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, nombre, apellido, contraseña=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nombre, apellido, contraseña, **extra_fields)


# -------------------------------
# MODELO DE ROL
# -------------------------------
class Rol(models.Model):
    idRol = models.AutoField(primary_key=True)
    nombreRol = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombreRol


# -------------------------------
# MODELO DE USUARIO PERSONALIZADO
# -------------------------------
class Usuario(AbstractBaseUser, PermissionsMixin):
    idUsuario = models.AutoField(primary_key=True)
    fotoPerfil = models.URLField(max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    telefonoAlt = models.CharField(max_length=20, blank=True, null=True)
    fechaRegistro = models.DateTimeField(default=timezone.now)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    notiC = models.BooleanField(default=False)
    notiW = models.BooleanField(default=False)
    modoOscuro = models.BooleanField(default=False)

    # Campos requeridos por Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"
