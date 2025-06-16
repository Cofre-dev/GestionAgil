from django.db import models

# Create your models here.
# tasks/models.py
from django.db import models

class ItemInventario(models.Model):
    # RF1: Registro de Inventario
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    numero_serie = models.CharField(max_length=100, unique=True, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    cantidad = models.IntegerField(default=0)
    umbral_minimo = models.IntegerField(default=5) # Para RF3: Alertas de Stock Bajo
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    categorias = models.ManyToManyField('Categoria', blank=True, related_name='items')
    etiquetas = models.ManyToManyField('Etiqueta', blank=True, related_name='items')

    def __str__(self):
        return f"{self.nombre} ({self.numero_serie or 'N/A'})"

    class Meta:
        verbose_name = "Item de Inventario"
        verbose_name_plural = "Items de Inventario"
        
        
class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('transferencia', 'Transferencia'),
        ('ajuste', 'Ajuste'),
    ]
    
    # RF2: Seguimiento de Movimiento de Inventarios
    item = models.ForeignKey(ItemInventario, on_delete=models.CASCADE, related_name='movimientos')
    tipo_movimiento = models.CharField(max_length=15, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad_cambio = models.IntegerField()
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    razon = models.TextField(blank=True, null=True)
    # Puedes añadir un usuario que realizó el movimiento si implementas autenticación de usuarios
    # usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo_movimiento.capitalize()} de {self.cantidad_cambio} de {self.item.nombre} el {self.fecha_movimiento.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
        ordering = ['-fecha_movimiento'] # Ordenar por fecha descendente por defecto
        
class Lote(models.Model):
    # RF4: Control de Lotes y Fechas de Vencimiento
    item = models.ForeignKey(ItemInventario, on_delete=models.CASCADE, related_name='lotes')
    numero_lote = models.CharField(max_length=100, unique=True)
    cantidad = models.IntegerField(default=0)
    fecha_vencimiento = models.DateField(blank=True, null=True) # Solo para ítems que expiran
    fecha_recepcion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Lote {self.numero_lote} de {self.item.nombre}"

    class Meta:
        verbose_name = "Lote"
        verbose_name_plural = "Lotes"
        # Asegura que no haya dos lotes con el mismo número para el mismo ítem (redundante con unique=True, pero útil para claridad)
        unique_together = ('item', 'numero_lote')
        
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"