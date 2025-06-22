from django.shortcuts import render
# tasks/views.py
from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
                                                                                
from .models import *
from .serializers import *
from .filters import ItemInventarioFilter 

class ItemInventarioListCreateView(generics.ListCreateAPIView):
    queryset = ItemInventario.objects.all()
    serializer_class = ItemInventarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ubicacion', 'stock_bajo', 'categorias', 'etiquetas'] 
    search_fields = ['nombre', 'descripcion', 'numero_serie']
    ordering_fields = ['nombre', 'cantidad', 'fecha_registro']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ItemInventarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ItemInventario.objects.all()
    serializer_class = ItemInventarioSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
# Nuevas vistas para Movimientos de Inventario
class MovimientoInventarioListCreateView(generics.ListCreateAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Opcional: para actualizar la cantidad del ItemInventario cuando se crea un movimiento
    def perform_create(self, serializer):
        movimiento = serializer.save()
        item = movimiento.item
        if movimiento.tipo_movimiento == 'entrada':
            item.cantidad += movimiento.cantidad_cambio
        elif movimiento.tipo_movimiento == 'salida':
            item.cantidad -= movimiento.cantidad_cambio
        item.save()

class MovimientoInventarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        old_movimiento = self.get_object() 
        new_movimiento = serializer.save() 

        item = new_movimiento.item

        if old_movimiento.tipo_movimiento == 'entrada':
            item.cantidad -= old_movimiento.cantidad_cambio
        elif old_movimiento.tipo_movimiento == 'salida':
            item.cantidad += old_movimiento.cantidad_cambio

        if new_movimiento.tipo_movimiento == 'entrada':
            item.cantidad += new_movimiento.cantidad_cambio
        elif new_movimiento.tipo_movimiento == 'salida':
            item.cantidad -= new_movimiento.cantidad_cambio

        item.save()

    def perform_destroy(self, instance):
        item = instance.item
        if instance.tipo_movimiento == 'entrada':
            item.cantidad -= instance.cantidad_cambio
        elif instance.tipo_movimiento == 'salida':
            item.cantidad += instance.cantidad_cambio
        item.save()
        instance.delete()

class LoteListCreateView(generics.ListCreateAPIView):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoriaListCreateView(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoriaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EtiquetaListCreateView(generics.ListCreateAPIView):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EtiquetaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class HistorialPrecioListCreateView(generics.ListCreateAPIView):
    queryset = HistorialPrecio.objects.all()
    serializer_class = HistorialPrecioSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class HistorialPrecioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistorialPrecio.objects.all()
    serializer_class = HistorialPrecioSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class KitListCreateView(generics.ListCreateAPIView):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class KitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class KitComponenteListCreateView(generics.ListCreateAPIView):
    queryset = KitComponente.objects.all()
    serializer_class = KitComponenteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class KitComponenteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KitComponente.objects.all()
    serializer_class = KitComponenteSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProveedorListCreateView(generics.ListCreateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProveedorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class ItemInventarioListCreateView(generics.ListCreateAPIView):
    queryset = ItemInventario.objects.all()
    serializer_class = ItemInventarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ItemInventarioFilter, 
    search_fields = ['nombre', 'descripcion', 'numero_serie']
    ordering_fields = ['nombre', 'cantidad', 'fecha_registro']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

