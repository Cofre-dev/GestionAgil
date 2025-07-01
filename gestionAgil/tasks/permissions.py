from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import generics
from django.views import generic

class IsGestorOrAdmin(BasePermission):
    
    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True
        
        return request.user.is_staff or request.user.groups.filter(name="Gestor de inventario").exists()
    
class ItemInventarioListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsGestorOrAdmin]
    
class ItemInventarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    Permission_classes = [IsGestorOrAdmin]

def _is_in_group(user, group_name):
    """
    Verifica si un usuario pertenece a un grupo específico.
    """
    return user.groups.filter(name=group_name).exists()

class IsAdminUser(BasePermission):
    """
    Permiso que solo permite el acceso a usuarios que son administradores (staff).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsGestorInventario(BasePermission):
    """
    Permiso para el Gestor de Inventario.
    Permite acceso total (CRUD) a la gestión de inventario (Items, Movimientos, Lotes, etc.).
    """
    def has_permission(self, request, view):
        return _is_in_group(request.user, 'Gestor de Inventario')

class IsComprador(BasePermission):
    """
    Permiso para el Comprador.
    Permite acceso de lectura a los ítems y gestión completa de Proveedores e Historial de Precios.
    """
    def has_permission(self, request, view):
        return _is_in_group(request.user, 'Comprador')

class ReadOnly(BasePermission):
    """
    Permiso que solo permite acciones de lectura (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS