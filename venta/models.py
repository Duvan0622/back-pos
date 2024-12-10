from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator

class Cliente(models.Model):
    documento = models.BigIntegerField(unique=True)
    nombre = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    celular = models.BigIntegerField(blank=True, null=True, validators=[MaxValueValidator(9999999999)] ) 

    def __str__(self):
        return f"{self.nombre} - {self.documento}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Factura(models.Model):
    numero_factura = models.AutoField(primary_key=True) 
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sucursal = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Factura {self.numero_factura} - Sucursal {self.sucursal} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"


class DetallesFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    class Meta:
        unique_together = (('factura', 'producto'),)

    def __str__(self):
        return f"Detalle de Factura {self.factura.numero_factura} - {self.producto.nombre}"

    def save(self, *args, **kwargs):
        self.precio_unitario = self.producto.precio
        self.precio_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
