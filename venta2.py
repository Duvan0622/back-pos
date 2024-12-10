import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fromages_back.settings')
django.setup()

from rest_framework.test import APIClient
from django.urls import reverse

client = APIClient()

login_url = reverse("login")
login_data = {"nombre_usuario": "juanP", "password": "Juan123"}
login_response = client.post(login_url, login_data, format='json')

if login_response.status_code == 200:
    token = login_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
else:
    print("Error en la autenticación:", login_response.json())
    exit()


cliente_id = 2
producto1_id = 1
producto2_id = 29
producto3_id = 18

data = {
    "cliente_id": cliente_id,
    "productos": [
        {"producto_id": producto1_id, "cantidad": 2},
        {"producto_id": producto2_id, "cantidad": 1},
        {"producto_id": producto3_id, "cantidad": 4}
    ]
}

url_crear_venta = reverse("iniciar-venta")

response = client.post(url_crear_venta, data, format='json')

if response.status_code == 201:
    response_json = response.json()
    print("Venta creada exitosamente.")
    print(f"Número de Factura: {response_json.get('numero_factura')}")
    print(f"Total Factura: {response_json.get('total')}")
else:
    print("Error al crear la venta:", response.json())
