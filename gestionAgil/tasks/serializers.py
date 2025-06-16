# tasks/serializers.py
from rest_framework import serializers
from .models import *

class ItemInventarioSerializer(serializers.ModelSerializer):
    
    stock_bajo = serializers.SerializerMethodField()
    
    class Meta:
        model = ItemInventario
        fields = '__all__' # Incluye todos los campos del modelo
        
    def get_stock_bajo(self,obj):
        return obj.cantidad < obj.umbral_minimo

class MovimientoInventarioSerializer(serializers.ModelSerializer):
    # Puedes añadir una representación del item para que no solo muestre el ID
    item_nombre = serializers.ReadOnlyField(source='item.nombre')
    item_numero_serie = serializers.ReadOnlyField(source='item.numero_serie')

    class Meta:
        model = MovimientoInventario
        fields = '__all__'
        # O puedes especificar los campos que quieres incluir en la API
        # fields = ['id', 'item', 'item_nombre', 'item_numero_serie', 'tipo_movimiento', 'cantidad_cambio', 'fecha_movimiento', 'razon']

class LoteSerializer(serializers.ModelSerializer):
    item_nombre = serializers.ReadOnlyField(source='item.nombre')
    # Puedes añadir un campo para saber si el lote está vencido
    vencido = serializers.SerializerMethodField()

    class Meta:
        model = Lote
        fields = '__all__'

    def get_vencido(self, obj):
        if obj.fecha_vencimiento:
            # Importa datetime en la parte superior del archivo si no lo has hecho
            from datetime import date
            return obj.fecha_vencimiento < date.today()
        return False