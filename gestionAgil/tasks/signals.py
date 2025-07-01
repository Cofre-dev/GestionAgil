from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
import datetime

@receiver(post_save, sender=ItemInventario)
def verificar_stock_bajo(sender, instance, created, **kwargs):
   
    # Comprobamos si el stock es bajo
    stock_es_bajo = instance.cantidad < instance.umbral_minimo
    
    if stock_es_bajo:
         
        # Por ahora, simularemos la alerta imprimiendo un mensaje en la consola del servidor.
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("-----------------------------------------------------------")
        print(f"🚨 ALERTA DE STOCK BAJO - {timestamp} 🚨")
        print(f"   Ítem: {instance.nombre} (ID: {instance.id})")
        print(f"   Cantidad actual: {instance.cantidad}")
        print(f"   Umbral mínimo: {instance.umbral_minimo}")
        print("   Se necesita reposición inmediata.")
        print("-----------------------------------------------------------")
