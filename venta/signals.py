from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Factura, DetallesFactura
from django.db.models import Max
from django.db.models import Sum

@receiver(post_save, sender=DetallesFactura)
@receiver(post_delete, sender=DetallesFactura)
def actualizar_total_factura(sender, instance, **kwargs):
    factura = instance.factura
    total = factura.detalles.aggregate(Sum('precio_total'))['precio_total__sum'] or 0
    factura.total = total
    factura.save()