from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cliente, Producto, Factura, DetallesFactura
from .serializers import ClienteSerializer, ProductoSerializer, FacturaSerializer, CrearVentaSerializer
from rest_framework import status, generics
from django.db import transaction
from rest_framework import serializers
from django.db.models import Max
from rest_framework.permissions import BasePermission

class ClienteView(APIView):
    def get(self, request, documento):
        cliente = Cliente.objects.filter(documento=documento).first()
        if cliente:
            serializer = ClienteSerializer(cliente)
            return Response(serializer.data)
        return Response({'error': 'Cliente no encontrado'}, status=404)

class ProductoView(APIView):
    def get(self, request):
        query = request.GET.get('query')
        if query:
            productos = Producto.objects.filter(nombre__icontains=query) | Producto.objects.filter(id=query)
        else:
            productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    
class IsVendedorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.rol == "vendedor"

class IniciarVentaView(APIView):
    permission_classes = [IsVendedorPermission]

    def post(self, request):
        serializer = CrearVentaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            factura = serializer.save()
            factura_serializer = FacturaSerializer(factura)
            return Response(factura_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoList(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        codigo = self.request.query_params.get('codigo', None) #Faltaba esto para la tabla productos
        nombre = self.request.query_params.get('nombre', None)
        precio = self.request.query_params.get('precio', None)
        stock = self.request.query_params.get('stock', None)
        

        if codigo:
            queryset = queryset.filter(id_producto=codigo)
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if precio:
            queryset = queryset.filter(precio__gte=precio)
        if stock:
            queryset = queryset.filter(stock__gte=stock)
        return queryset

# metodo para restar del stock al momento de agregar el producto a la factura
class APaF(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def put(self, request, *args, **kwargs):

        # valida que exista el producto
        try:
            producto = Producto.objects.get(pk=self.kwargs['id_producto'])
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        # cantidad es el dato que recibe de Geiner 
        cantidad_a_restar = request.data.get('cantidad')
       
        nuevo_stock = producto.stock - int(cantidad_a_restar)

        if nuevo_stock > producto.stock:
            return Response({"error": "No hay stock disponible para la cantidad solicitada"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            producto.stock = nuevo_stock
            producto.save()
              
        serializer = ProductoSerializer(producto)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# metodo para que al eliminar un producto se libere el stock 
class EPaF(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def put(self, request, *args, **kwargs):

        # valida que exista el producto
        try:
            producto = Producto.objects.get(pk=self.kwargs['id_producto'])
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        # cantidad es el dato que recibe de Geiner 
        cantidad_a_agregar = request.data.get('cantidad')
       
        nuevo_stock = producto.stock + int(cantidad_a_agregar)

        producto.stock = nuevo_stock
        producto.save()
   
        serializer = ProductoSerializer(producto)
        return Response(serializer.data, status=status.HTTP_200_OK)