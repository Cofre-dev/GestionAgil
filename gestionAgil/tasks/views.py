from django.shortcuts import render
# tasks/views.py
from rest_framework import generics, filters, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
                                                                                
from .models import *
from .serializers import *
from .filters import ItemInventarioFilter 
from .permissions import *

def vista_login(request):
    return render(request, 'index.html')

def vista_inventario(request):
    return render(request, 'inventario.html')
    
class ItemInventarioListCreateView(generics.ListCreateAPIView):
    queryset = ItemInventario.objects.all()
    serializer_class = ItemInventarioSerializer
    filterset_class = ItemInventarioFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion','numero_serie']
    ordering_fields = ['nombre', 'cantidad', 'fecha_registro']
    permission_classes = [IsAdminUser | IsGestorInventario]
    # lookup_field = 'pk'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
       
class ItemInventarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ItemInventario.objects.all()
    serializer_class = ItemInventarioSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser | IsGestorInventario]

class MovimientoInventarioListCreateView(generics.ListCreateAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
    permission_classes = [IsAdminUser | IsGestorInventario]

    def perform_create(self, serializer):
        movimiento = serializer.save()
        item = movimiento.item
        if movimiento.tipo_movimiento == 'entrada':
            item.cantidad += movimiento.cantidad_cambio
        elif movimiento.tipo_movimiento == 'salida':
            item.cantidad -= movimiento.cantidad_cambio
        item.save()
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        item = serializer.validated_data['item']
        cantidad_cambio = serializer.validated_data['cantidad_cambio']
        tipo_movimiento = serializer.validated_data['tipo_movimiento']
        
        if tipo_movimiento == 'salida' and item.cantidad < cantidad_cambio:
            return Response(
                {"error": f"Stock insuficiente para '{item.nombre}'. Stock actual: {item.cantidad}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        movimiento = serializer.save()
        if tipo_movimiento == 'entrada':
            item.cantidad += cantidad_cambio
        elif tipo_movimiento == 'salida':
            item.cantidad -= cantidad_cambio
        item.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MovimientoInventarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser | IsGestorInventario]

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
    permission_classes = [IsAdminUser | IsGestorInventario]

class LoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser | IsGestorInventario]

class CategoriaListCreateView(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAdminUser | IsGestorInventario]

class CategoriaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser | IsGestorInventario]

class EtiquetaListCreateView(generics.ListCreateAPIView):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    permission_classes = [IsAdminUser | IsGestorInventario]

class EtiquetaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser | IsGestorInventario]

class HistorialPrecioListCreateView(generics.ListCreateAPIView):
    queryset = HistorialPrecio.objects.all()
    serializer_class = HistorialPrecioSerializer
    permission_classes = [IsAdminUser | IsGestorInventario]

class HistorialPrecioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistorialPrecio.objects.all()
    serializer_class = HistorialPrecioSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser | IsGestorInventario]

class KitListCreateView(generics.ListCreateAPIView):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer
    permission_classes = [IsAdminUser | IsGestorInventario]

class KitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser | IsGestorInventario]

class KitComponenteListCreateView(generics.ListCreateAPIView):
    queryset = KitComponente.objects.all()
    serializer_class = KitComponenteSerializer
    permission_classes = [IsAdminUser | IsGestorInventario]
    
class KitComponenteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KitComponente.objects.all()
    serializer_class = KitComponenteSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser | IsGestorInventario]

class ProveedorListCreateView(generics.ListCreateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAdminUser | IsGestorInventario]

class ProveedorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser | IsGestorInventario]