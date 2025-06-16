# tasks/urls.py
from django.urls import path
from . import views

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
]