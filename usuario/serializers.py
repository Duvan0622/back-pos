from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        user = Usuario
        token = super().get_token(user)
        token['nombre_usuario'] = user.nombre_usuario
        token['role'] = user.rol
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            "rol": self.user.rol  
        })
        return data

class LoginSerializer(serializers.Serializer):
    nombre_usuario = serializers.CharField()  
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        nombre_usuario = data.get('nombre_usuario')
        password = data.get('password')
        user = authenticate(username=nombre_usuario, password=password)
        
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credenciales incorrectas o usuario inactivo.")


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'documento', 'nombre', 'nombre_usuario', 'rol']
        extra_kwargs = {'password': {'write_only': True}}

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        RefreshToken(self.token).blacklist()
