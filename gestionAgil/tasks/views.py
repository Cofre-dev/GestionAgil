from django.shortcuts import render
# tasks/views.py
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend # ¡Importa esto!                                                                                                                                                                
from .models import *
from .serializers import *
from .filters import ItemInventarioFilter 

class ItemInventarioListCreateView(generics.ListCreateAPIView):
    queryset = ItemInventario.objects.all()
    serializer_class = ItemInventarioSerializer
    # Nuevas configuraciones para filtrado y búsqueda
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ubicacion', 'stock_bajo', 'categorias', 'etiquetas'] # Campos por los que se puede filtrar
    search_fields = ['nombre', 'descripcion', 'numero_serie'] # Campos por los que se puede buscar texto
    ordering_fields = ['nombre', 'cantidad', 'fecha_registro'] # Campos por los que se puede ordenar    

class ItemInventarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # Esta vista permite recuperar, actualizar y eliminar un ItemInventario específico
    # (GET para un ID, PUT/PATCH para actualizar, DELETE para eliminar)
    queryset = ItemInventario.objects.all()
    serializer_class = ItemInventarioSerializer
    lookup_field = 'pk' # Por defecto es 'pk' (primary key), pero lo especificamos por claridad
    
# Nuevas vistas para Movimientos de Inventario
class MovimientoInventarioListCreateView(generics.ListCreateAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer

    # Opcional: para actualizar la cantidad del ItemInventario cuando se crea un movimiento
    def perform_create(self, serializer):
        movimiento = serializer.save()
        item = movimiento.item
        if movimiento.tipo_movimiento == 'entrada':
            item.cantidad += movimiento.cantidad_cambio
        elif movimiento.tipo_movimiento == 'salida':
            item.cantidad -= movimiento.cantidad_cambio
        # Aquí podrías añadir lógica para transferencia o ajuste
        item.save()

class MovimientoInventarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
    lookup_field = 'pk'

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
        # Revertir el cambio al eliminar el movimiento
        if instance.tipo_movimiento == 'entrada':
            item.cantidad -= instance.cantidad_cambio
        elif instance.tipo_movimiento == 'salida':
            item.cantidad += instance.cantidad_cambio
        item.save()
        instance.delete()

class LoteListCreateView(generics.ListCreateAPIView):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

class LoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    lookup_field = 'pk'

class CategoriaListCreateView(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    lookup_field = 'pk'

class EtiquetaListCreateView(generics.ListCreateAPIView):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer

class EtiquetaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    lookup_field = 'pk'

class HistorialPrecioListCreateView(generics.ListCreateAPIView):
    queryset = HistorialPrecio.objects.all()
    serializer_class = HistorialPrecioSerializer

class HistorialPrecioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistorialPrecio.objects.all()
    serializer_class = HistorialPrecioSerializer
    lookup_field = 'pk'

class KitListCreateView(generics.ListCreateAPIView):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer

class KitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer
    lookup_field = 'pk'

class KitComponenteListCreateView(generics.ListCreateAPIView):
    queryset = KitComponente.objects.all()
    serializer_class = KitComponenteSerializer

class KitComponenteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KitComponente.objects.all()
    serializer_class = KitComponenteSerializer
    lookup_field = 'pk'

class ProveedorListCreateView(generics.ListCreateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ProveedorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    lookup_field = 'pk'
    
class ItemInventarioListCreateView(generics.ListCreateAPIView):
    queryset = ItemInventario.objects.all()
    serializer_class = ItemInventarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ItemInventarioFilter # <-- ¡Cambia esto de filterset_fields a filterset_class!
    search_fields = ['nombre', 'descripcion', 'numero_serie']
    ordering_fields = ['nombre', 'cantidad', 'fecha_registro']