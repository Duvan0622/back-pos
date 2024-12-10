from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento', 'rol', 'nombre_usuario', 'is_active', 'is_staff')
    ordering = ['nombre_usuario']  