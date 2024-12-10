import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fromages_back.settings')  
django.setup()

from usuario.models import Usuario

usuarios = [
    {'documento': '1890786576', 'nombre': 'Juan Perez', 'nombre_usuario': 'juanP', 'password': 'Juan123', 'rol': 'vendedor'},
    {'documento': '1298765477', 'nombre': 'Maria Lopez', 'nombre_usuario': 'mariaL', 'password': 'Maria123', 'rol': 'vendedor'},
    {'documento': '1009876567', 'nombre': 'Pedro Martinez', 'nombre_usuario': 'pedroM', 'password': 'Pedro123', 'rol': 'vendedor'},
    {'documento': '987465267', 'nombre': 'Mario Torres', 'nombre_usuario': 'marioT', 'password': 'Mario123', 'rol': 'vendedor'},
    {'documento': '356678333', 'nombre': 'Veronica Mendoza', 'nombre_usuario': 'veronicaM', 'password': 'Veronica123', 'rol': 'vendedor'},
    {'documento': '453824568', 'nombre': 'Pablo Martinez', 'nombre_usuario': 'pabloM', 'password': 'Pablo123', 'rol': 'vendedor'},
    {'documento': '546457483', 'nombre': 'Diego Paez', 'nombre_usuario': 'diegoP', 'password': 'Diego123', 'rol': 'vendedor'},
    {'documento': '377935645', 'nombre': 'Juan Ramirez', 'nombre_usuario': 'juanR', 'password': 'JuanR123', 'rol': 'vendedor'},
    {'documento': '573673884', 'nombre': 'Maria Ortega', 'nombre_usuario': 'mariaO', 'password': 'MariaO123', 'rol': 'vendedor'},
    {'documento': '324567891', 'nombre': 'Urbano Gomez', 'nombre_usuario': 'urbanoG', 'password': 'UrbanoAdmin', 'rol': 'gerente'},
]

for user_data in usuarios:
    usuario = Usuario(
        documento=user_data['documento'],
        nombre=user_data['nombre'],
        nombre_usuario=user_data['nombre_usuario'],
        rol=user_data['rol']
    )
    usuario.set_password(user_data['password'])  
    usuario.save()
