from django.db import models

# Create your models here.
# tasks/models.py
from django.db import models

class ItemInventario(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    numero_serie = models.CharField(max_length=100, unique=True, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    cantidad = models.IntegerField(default=0)
    umbral_minimo = models.IntegerField(default=5)
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
        
class HistorialPrecio(models.Model):
    item = models.ForeignKey(ItemInventario, on_delete=models.CASCADE, related_name='historial_precios')
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Precio de {self.item.nombre}: {self.precio_compra} el {self.fecha_registro}"

    class Meta:
        verbose_name = "Historial de Precio"
        verbose_name_plural = "Historial de Precios"
        ordering = ['-fecha_registro']
        
class Kit(models.Model):
    # RF8: Gestión de Kits y Conjuntos
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    # Un kit puede estar compuesto de otros kits (relación recursiva)
    componentes_kits = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='parent_kits')
    # Un kit también puede estar compuesto de ítems de inventario individuales
    componentes_items = models.ManyToManyField(ItemInventario, through='KitComponente', related_name='kits')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Kit"
        verbose_name_plural = "Kits"

# Modelo intermedio para la relación Many-to-Many con atributos adicionales (cantidad)
class KitComponente(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemInventario, on_delete=models.CASCADE)
    cantidad_requerida = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad_requerida}x {self.item.nombre} en {self.kit.nombre}"

    class Meta:
        unique_together = ('kit', 'item') 
        verbose_name = "Componente de Kit"
        verbose_name_plural = "Componentes de Kits"
    
class Proveedor(models.Model):
    # RF10: Gestión de Proveedores
    nombre = models.CharField(max_length=200, unique=True)
    contacto_principal = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    terminos_pago = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"