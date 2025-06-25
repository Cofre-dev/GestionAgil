
# gestionAgil/gestionAgil/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken import views as authtoken_views

# Importaciones para drf-yasg
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Para servir archivos HTML (templates)
from django.views.generic import TemplateView # <--- Importa esto
from django.conf import settings # <--- Importa settings
from django.conf.urls.static import static # <--- Importa esto para staticfiles en desarrollo

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
    path('api-token-auth/', authtoken_views.obtain_auth_token), 
    path('api/', include('tasks.urls')),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('', TemplateView.as_view(template_name='index.html'), name='home'), 
]

