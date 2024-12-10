import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fromages_back.settings')
django.setup()

from venta.models import Cliente, Producto, Factura, DetallesFactura
from django.contrib.auth import get_user_model
from django.db.models import Max
from django.db.models import Sum
from django.db import connection

User = get_user_model()

facturas_data = [
    {'cliente_id': 1, 'vendedor_id': 1},
    {'cliente_id': 2, 'vendedor_id': 2},
    {'cliente_id': 3, 'vendedor_id': 3},
    {'cliente_id': 4, 'vendedor_id': 4},
    {'cliente_id': 5, 'vendedor_id': 5},
    {'cliente_id': 6, 'vendedor_id': 6},
    {'cliente_id': 7, 'vendedor_id': 7},
    {'cliente_id': 8, 'vendedor_id': 8},
    {'cliente_id': 9, 'vendedor_id': 9},
]

ultimo_numero_factura = Factura.objects.aggregate(Max('numero_factura'))['numero_factura__max'] or 0

facturas_creadas = []
facturas_map = {}  
for factura_data in facturas_data:
    cliente = Cliente.objects.get(id=factura_data['cliente_id'])
    vendedor = User.objects.get(id=factura_data['vendedor_id'])
    ultimo_numero_factura += 1
    factura = Factura.objects.create(numero_factura=ultimo_numero_factura, cliente=cliente, vendedor=vendedor)
    facturas_creadas.append(factura)
    facturas_map[factura.cliente.id] = factura 

detalles_factura_data = [
    {'cliente_id': 1, 'producto_id': 1, 'cantidad': 2},
    {'cliente_id': 1, 'producto_id': 2, 'cantidad': 1},
    {'cliente_id': 2, 'producto_id': 3, 'cantidad': 3},
    {'cliente_id': 2, 'producto_id': 4, 'cantidad': 2},
    {'cliente_id': 3, 'producto_id': 5, 'cantidad': 1},
    {'cliente_id': 3, 'producto_id': 6, 'cantidad': 2},
    {'cliente_id': 4, 'producto_id': 7, 'cantidad': 1},
    {'cliente_id': 4, 'producto_id': 8, 'cantidad': 1},
    {'cliente_id': 5, 'producto_id': 9, 'cantidad': 2},
    {'cliente_id': 5, 'producto_id': 10, 'cantidad': 3},
    {'cliente_id': 6, 'producto_id': 11, 'cantidad': 3},
    {'cliente_id': 6, 'producto_id': 12, 'cantidad': 2},
    {'cliente_id': 7, 'producto_id': 13, 'cantidad': 1},
    {'cliente_id': 7, 'producto_id': 14, 'cantidad': 4},
    {'cliente_id': 8, 'producto_id': 15, 'cantidad': 2},
    {'cliente_id': 8, 'producto_id': 16, 'cantidad': 1},
    {'cliente_id': 9, 'producto_id': 17, 'cantidad': 1},
    {'cliente_id': 9, 'producto_id': 18, 'cantidad': 4},
    {'cliente_id': 9, 'producto_id': 19, 'cantidad': 1},
    {'cliente_id': 9, 'producto_id': 20, 'cantidad': 2},
    {'cliente_id': 9, 'producto_id': 22, 'cantidad': 3},
    {'cliente_id': 9, 'producto_id': 30, 'cantidad': 4},
]

detalles = []
for detalle_data in detalles_factura_data:
    cliente_id = detalle_data['cliente_id']
    factura = facturas_map.get(cliente_id)
    if not factura:
        continue  

    producto = Producto.objects.get(id=detalle_data['producto_id'])
    cantidad = detalle_data['cantidad']
    precio_unitario = producto.precio
    detalles.append(DetallesFactura(
        factura=factura,
        producto=producto,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        precio_total=cantidad * precio_unitario
    ))

DetallesFactura.objects.bulk_create(detalles)

for factura in facturas_creadas:
    total = factura.detalles.aggregate(Sum('precio_total'))['precio_total__sum'] or 0
    factura.total = total
    factura.save()

print("Datos de facturas y detalles de facturas poblados correctamente.")

def sincronizar_secuencia():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT setval(pg_get_serial_sequence('venta_factura', 'numero_factura'), 
                         (SELECT MAX(numero_factura) FROM venta_factura))
        """)
    print("Secuencia sincronizada correctamente.")

if __name__ == "__main__":
    sincronizar_secuencia()
