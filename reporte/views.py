from urllib import request
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from venta.models import Factura, DetallesFactura, Cliente
from .serializers import FacturaDetalleSerializer, FacturaSerializer, DetallesFacturaSerializer
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny


class ReporteView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        # Recuperar los parámetros de la consulta
        fecha_inicio = request.query_params.get("fecha_inicio")
        fecha_fin = request.query_params.get("fecha_fin")
        sucursal = request.query_params.get("sucursal")  # Parámetro sucursal

        # Verificar que ambas fechas estén presentes
        if not fecha_inicio or not fecha_fin:
            return Response({"error": "Las fechas de inicio y fin son obligatorias"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convertir las fechas a formato datetime.date
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Formato de fecha incorrecto, usa YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar las facturas según las fechas
        facturas = Factura.objects.filter(fecha__date__range=[fecha_inicio, fecha_fin])

        # Filtrar por sucursal si se proporciona
        if sucursal:
            try:
                sucursal = int(sucursal)  # Convertir "sucursal" a entero
                facturas = facturas.filter(sucursal=sucursal)  # Filtrar por sucursal
            except ValueError:
                return Response({"error": "El valor de 'sucursal' debe ser un número entero."}, status=status.HTTP_400_BAD_REQUEST)

        # Serializar las facturas
        serializer = FacturaSerializer(facturas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SucursalListView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request):
        sucursales = [
            {"id": "1", "nombre": "Fromages"}
        ]
        return Response(sucursales)
    
class FacturaDetalleView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request, numero_factura):
        try:
            factura = Factura.objects.get(numero_factura=numero_factura)
            serializer = FacturaDetalleSerializer(factura)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Factura.DoesNotExist:
            return Response({"error": "Factura no encontrada."}, status=status.HTTP_404_NOT_FOUND)

class ReporteFacturasView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request):
        fecha_inicio = request.query_params.get("fecha_inicio")
        fecha_fin = request.query_params.get("fecha_fin")

        if not fecha_inicio or not fecha_fin:
            return Response({"error": "Por favor proporciona ambas fechas (inicio y fin) en formato YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        facturas = Factura.objects.filter(
            fecha__date__range=[fecha_inicio, fecha_fin]
        ).annotate(total_factura=Sum('detalles__precio_total'))

        serializer = FacturaSerializer(facturas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FacturaListView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request):
        # Obtener el vendedor_id desde el usuario autenticado
        vendedor_id = request.user.id  # Suponiendo que el vendedor es el usuario autenticado

        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        # Filtrar facturas por vendedor_id
        facturas = Factura.objects.filter(vendedor_id=vendedor_id)

        # Filtrar por fechas si están presentes
        if fecha_inicio and fecha_fin:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Formato de fecha incorrecto, usa YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
            
            facturas = facturas.filter(fecha__date__range=[fecha_inicio, fecha_fin])

        # Serializar y devolver las facturas
        serializer = FacturaSerializer(facturas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

