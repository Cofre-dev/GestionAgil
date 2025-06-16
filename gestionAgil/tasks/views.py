from django.shortcuts import render
# tasks/views.py
from rest_framework import generics
from .models import *
from .serializers import *

class ItemInventarioListCreateView(generics.ListCreateAPIView):
    # Esta vista permite listar todos los ItemInventario (GET) y crear uno nuevo (POST)
    queryset = ItemInventario.objects.all()
    serializer_class = ItemInventarioSerializer

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

    # Opcional: para actualizar la cantidad del ItemInventario cuando se actualiza o elimina un movimiento
    def perform_update(self, serializer):
        old_movimiento = self.get_object() # Obtiene el objeto antes de la actualización
        new_movimiento = serializer.save() # Guarda el nuevo objeto

        item = new_movimiento.item

        # Revertir el cambio anterior
        if old_movimiento.tipo_movimiento == 'entrada':
            item.cantidad -= old_movimiento.cantidad_cambio
        elif old_movimiento.tipo_movimiento == 'salida':
            item.cantidad += old_movimiento.cantidad_cambio

        # Aplicar el nuevo cambio
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
        
# Nuevas vistas para Lotes
class LoteListCreateView(generics.ListCreateAPIView):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

class LoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    lookup_field = 'pk'