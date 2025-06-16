# tasks/admin.py
from django.contrib import admin
from .models import *

# Registra tu modelo aquí
admin.site.register(ItemInventario)
admin.site.register(MovimientoInventario)
admin.site.register(Lote)
admin.site.register(Categoria) 
admin.site.register(Etiqueta) 