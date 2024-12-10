import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fromages_back.settings') 
django.setup()

from venta.models import Factura

def sincronizar_secuencia():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT setval(pg_get_serial_sequence('venta_factura', 'numero_factura'), 
                         (SELECT MAX(numero_factura) FROM venta_factura))
        """)
    print("Secuencia sincronizada correctamente.")

if __name__ == "__main__":
    sincronizar_secuencia()
