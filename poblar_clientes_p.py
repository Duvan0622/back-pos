import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fromages_back.settings') 

django.setup()

from venta.models import Cliente, Producto

clientes = [
    {'documento': '1890786576', 'nombre': 'Juan Alban', 'email': 'juanalban@gmail.com', 'celular': '3201234567'},
    {'documento': '1298765477', 'nombre': 'Maria Cordero', 'email': 'mariacordero@outlook.com', 'celular': '3152345678'},
    {'documento': '1009876567', 'nombre': 'Pedro Pinto', 'email': 'pedropinto@gmail.com', 'celular': '3143456789'},
    {'documento': '1876090006', 'nombre': 'Pablo Ponce', 'email': 'pabloponce@outlook.com', 'celular': '3164567890'},
    {'documento': '1893456776', 'nombre': 'Lorena Paz', 'email': 'lorenapaz@gmail.com', 'celular': '3205678901'},
    {'documento': '1678999891', 'nombre': 'Rosario Utreras', 'email': 'rosarioutreras@outlook.com', 'celular': '3156789012'},
    {'documento': '1244567888', 'nombre': 'Leticia Ortega', 'email': 'leticiaortega@gmail.com', 'celular': '3147890123'},
    {'documento': '1456799022', 'nombre': 'Juan Torres', 'email': 'juantorres@outlook.com', 'celular': '3168901234'},
    {'documento': '1845677777', 'nombre': 'Jorge Parra', 'email': 'jorgeparra@gmail.com', 'celular': '3209012345'},
    {'documento': '183445667', 'nombre': 'Pablo Polit', 'email': 'pablopolit@outlook.com', 'celular': '3151234567'},
]

for cliente_data in clientes:
    Cliente.objects.create(**cliente_data)

productos = [
    {'nombre': 'Queso Doble Crema', 'precio': 8000, 'stock': 60},
    {'nombre': 'Queso Mozzarella', 'precio': 9500, 'stock': 32},
    {'nombre': 'Queso Campesino', 'precio': 6000, 'stock': 30},
    {'nombre': 'Queso Criollo', 'precio': 7500, 'stock': 17},
    {'nombre': 'Queso Costeño', 'precio': 8000, 'stock': 65},
    {'nombre': 'Queso Pera', 'precio': 11000, 'stock': 40},
    {'nombre': 'Queso Saravena', 'precio': 12000, 'stock': 30},
    {'nombre': 'Queso Gouda', 'precio': 15000, 'stock': 35},
    {'nombre': 'Queso Parmesano', 'precio': 14000, 'stock': 35},
    {'nombre': 'Queso Gruyere', 'precio': 17000, 'stock': 29},
    {'nombre': 'Queso Camembert', 'precio': 17500, 'stock': 24},
    {'nombre': 'Queso Provolone', 'precio': 13000, 'stock': 33},
    {'nombre': 'Queso Emmental', 'precio': 14000, 'stock': 24},
    {'nombre': 'Queso Brie', 'precio': 16000, 'stock': 29},
    {'nombre': 'Queso Cottage', 'precio': 15000, 'stock': 28},
    {'nombre': 'Queso Feta', 'precio': 15000, 'stock': 32},
    {'nombre': 'Queso Suizo', 'precio': 20000, 'stock': 15},
    {'nombre': 'Queso Manchego', 'precio': 18000, 'stock': 20},
    {'nombre': 'Queso Roquefort', 'precio': 21000, 'stock': 25},
    {'nombre': 'Queso Asiago', 'precio': 17000, 'stock': 30},
    {'nombre': 'Queso Cheddar', 'precio': 12000, 'stock': 40},
    {'nombre': 'Queso Edam', 'precio': 14000, 'stock': 28},
    {'nombre': 'Queso Halloumi', 'precio': 16000, 'stock': 25},
    {'nombre': 'Queso Mascarpone', 'precio': 19000, 'stock': 22},
    {'nombre': 'Queso Pecorino', 'precio': 21000, 'stock': 18},
    {'nombre': 'Queso Ricotta', 'precio': 10000, 'stock': 35},
    {'nombre': 'Queso Taleggio', 'precio': 18500, 'stock': 20},
    {'nombre': 'Queso Burrata', 'precio': 20000, 'stock': 15},
    {'nombre': 'Queso Cotija', 'precio': 13000, 'stock': 30},
    {'nombre': 'Queso Oaxaca', 'precio': 11000, 'stock': 40},
    {'nombre': 'Queso Panela', 'precio': 10500, 'stock': 45},
    {'nombre': 'Queso Stilton', 'precio': 22000, 'stock': 10},
]

for producto_data in productos:
    Producto.objects.create(**producto_data)
