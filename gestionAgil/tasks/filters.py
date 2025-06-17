# tasks/filters.py
import django_filters
from .models import ItemInventario, Lote, MovimientoInventario # Importa los modelos que vas a filtrar

class ItemInventarioFilter(django_filters.FilterSet):
    # Filtro para 'stock_bajo'
    # Puedes definirlo como BooleanFilter si quieres 'true'/'false'
    # O un NumberFilter si quieres filtrar por cantidad < X
    stock_bajo = django_filters.BooleanFilter(field_name='cantidad', lookup_expr='lt', method='filter_stock_bajo')

    # Filtro por rango de fechas de registro
    fecha_registro_min = django_filters.DateFilter(field_name='fecha_registro', lookup_expr='gte')
    fecha_registro_max = django_filters.DateFilter(field_name='fecha_registro', lookup_expr='lte')

    # Filtros para relaciones ManyToMany por ID
    categorias = django_filters.ModelMultipleChoiceFilter(
        queryset=ItemInventario.categorias.through.objects.all().values_list('categoria_id', flat=True).distinct(),
        field_name='categorias__id',
        to_field_name='id',
    )
    etiquetas = django_filters.ModelMultipleChoiceFilter(
        queryset=ItemInventario.etiquetas.through.objects.all().values_list('etiqueta_id', flat=True).distinct(),
        field_name='etiquetas__id',
        to_field_name='id',
    )

    class Meta:
        model = ItemInventario
        fields = {
            'ubicacion': ['exact'],
            'nombre': ['icontains'], # Permite buscar por parte del nombre
            'numero_serie': ['exact', 'icontains'],
            'cantidad': ['exact', 'gte', 'lte'], # Igual, mayor o igual, menor o igual
            'umbral_minimo': ['exact', 'gte', 'lte'],
        }

    def filter_stock_bajo(self, queryset, name, value):
        if value: # Si value es True
            return queryset.filter(cantidad__lt=models.F('umbral_minimo'))
        return queryset