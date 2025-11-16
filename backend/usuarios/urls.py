# usuarios/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, RolViewSet

# Creamos un router
router = DefaultRouter()
router.register(r'roles', RolViewSet)
router.register(r'usuarios', UsuarioViewSet)

# Las URLs de la API son determinadas automáticamente por el router
urlpatterns = [
    path('', include(router.urls)),
]