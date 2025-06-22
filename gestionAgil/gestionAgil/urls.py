
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import *
from django.conf import settings
from django.conf.urls.static import static

#Importaciones para drf-yasg
from rest_framework.authtoken import views as authtoken_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define el esquema de la API
schema_view = get_schema_view(
   openapi.Info(
      title="Maestranzas Unidos S.A. API de Inventario",
      default_version='v1',
      description="Documentación de la API para el Sistema de Control de Inventarios de Maestranzas Unidos S.A.",
      terms_of_service="https://www.google.com/policies/terms/", 
      contact=openapi.Contact(email="contacto@maestranzasunidos.com"), 
      license=openapi.License(name="BSD License"), 
   ),
   public=True,
   permission_classes=(permissions.AllowAny,), 
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
    path('api-token-auth', authtoken_views.obtain_auth_token),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Ruta para tu archivo HTML simple
    path('', TemplateView.as_view(template_name='index.html'), name='home'), # <--- ¡Añade esta línea!
]

