from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_usuario, documento, rol, nombre, password=None, **extra_fields):
        usuario = self.model(
            nombre_usuario=nombre_usuario,
            documento=documento,
            rol=rol,
            nombre=nombre,
            **extra_fields
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, nombre_usuario, documento, rol, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(nombre_usuario, documento, rol, nombre, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=30)
    documento = models.CharField(max_length=20, unique=True)
    rol = models.CharField(max_length=20)
    nombre_usuario = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'nombre_usuario'
    REQUIRED_FIELDS = ['documento', 'rol', 'nombre']

    def __str__(self):
        return self.nombre_usuario
