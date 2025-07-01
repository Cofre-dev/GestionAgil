# tasks/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *

# router = DefaultRouter()
# router.register(r'items', LoteListCreateView)

urlpatterns = [
    
     # URLs para Items de Inventario
    path('items/', views.ItemInventarioListCreateView.as_view(), name='iteminventario-list-create'),
    path('items/<int:pk>/', views.ItemInventarioRetrieveUpdateDestroyView.as_view(), name='iteminventario-detail'),

    # URLs para Movimientos de Inventario
    path('movements/', views.MovimientoInventarioListCreateView.as_view(), name='movimientoinventario-list-create'),
    path('movements/<int:pk>/', views.MovimientoInventarioRetrieveUpdateDestroyView.as_view(), name='movimientoinventario-detail'),

    # URLs para Lotes
    path('lotes/', views.LoteListCreateView.as_view(), name='lote-list-create'),
    path('lotes/<int:pk>/', views.LoteRetrieveUpdateDestroyView.as_view(), name='lote-detail'),

    # URLs para Categorias
    path('categories/', views.CategoriaListCreateView.as_view(), name='categoria-list-create'),
    path('categories/<int:pk>/', views.CategoriaRetrieveUpdateDestroyView.as_view(), name='categoria-detail'),

    # URLs para Etiquetas
    path('tags/', views.EtiquetaListCreateView.as_view(), name='etiqueta-list-create'),
    path('tags/<int:pk>/', views.EtiquetaRetrieveUpdateDestroyView.as_view(), name='etiqueta-detail'), 

     # URLs para Historial de Precios
    path('price-history/', views.HistorialPrecioListCreateView.as_view(), name='historialprecio-list-create'),
    path('price-history/<int:pk>/', views.HistorialPrecioRetrieveUpdateDestroyView.as_view(), name='historialprecio-detail'),

    # URLs para Kits
    path('kits/', views.KitListCreateView.as_view(), name='kit-list-create'),
    path('kits/<int:pk>/', views.KitRetrieveUpdateDestroyView.as_view(), name='kit-detail'),

    # URLs para Componentes de Kits (la tabla intermedia)
    path('kit-components/', views.KitComponenteListCreateView.as_view(), name='kitcomponente-list-create'),
    path('kit-components/<int:pk>/', views.KitComponenteRetrieveUpdateDestroyView.as_view(), name='kitcomponente-detail'),
    
     # URLs para Proveedores
    path('suppliers/', views.ProveedorListCreateView.as_view(), name='proveedor-list-create'),
    path('suppliers/<int:pk>/', views.ProveedorRetrieveUpdateDestroyView.as_view(), name='proveedor-detail'),
]
    


    



    

    
    
   
    
