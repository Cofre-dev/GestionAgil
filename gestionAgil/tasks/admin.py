# tasks/admin.py
#Probando el commit xd
from django.contrib import admin
from .models import *

# Registra tu modelo aquí
admin.site.register(ItemInventario)
admin.site.register(MovimientoInventario)
admin.site.register(Lote)
admin.site.register(Categoria) 
admin.site.register(Etiqueta)
admin.site.register(HistorialPrecio)
admin.site.register(Kit)
admin.site.register(KitComponente)
admin.site.register(Proveedor)

