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

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = '__all__'
        
class HistorialPrecioSerializer(serializers.ModelSerializer):
    item_nombre = serializers.ReadOnlyField(source='item.nombre')
    
    class Meta:
        model = HistorialPrecio
        fields = '__all__'
        
class KitComponenteSerializer(serializers.ModelSerializer):
    item_nombre = serializers.ReadOnlyField(source='item.nombre')
    item_numero_serie = serializers.ReadOnlyField(source='item.numero_serie')

    class Meta:
        model = KitComponente
        fields = ['id', 'item', 'item_nombre', 'item_numero_serie', 'cantidad_requerida']

class KitSerializer(serializers.ModelSerializer):
    # Para ver los IDs de los kits componentes anidados
    componentes_kits = serializers.PrimaryKeyRelatedField(many=True, queryset=Kit.objects.all(), required=False)
    # Para ver los detalles de los ítems componentes
    componentes_items_details = KitComponenteSerializer(source='kitcomponente_set', many=True, read_only=True)

    class Meta:
        model = Kit
        fields = '__all__'
        
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fiels = '__all__'
        
