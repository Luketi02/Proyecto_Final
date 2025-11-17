"""
URL configuration for prjct project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  
from django.urls import path
from django.urls import path
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
#Imports de apps
from reparaciones.views import DispositivoViewSet
from usuarios.views import UsuarioViewSet, RolViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')), 
]

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'roles', RolViewSet, basename='rol')
router.register(r'dispositivos', DispositivoViewSet, basename='dispositivo')

urlpatterns = [
    path('', RedirectView.as_view(url='/api/v1/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static('/', document_root=settings.FRONTEND_DIR)