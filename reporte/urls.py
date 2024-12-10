from django.urls import path
from .views import FacturaListView, ReporteView, SucursalListView, FacturaDetalleView

urlpatterns = [
    path('facturas/', ReporteView.as_view(), name="reporte-facturas"),  
    path('sucursales/', SucursalListView.as_view(), name="sucursal-list"),
    path('factura-detalle/<int:numero_factura>/', FacturaDetalleView.as_view(), name="factura-detalle"),
    path('factura-list/', FacturaListView.as_view(), name="factura-list"),
    
]
