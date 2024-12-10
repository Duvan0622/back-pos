from django.urls import path
from .views import IniciarVentaView, ClienteView, ProductoView, APaF, EPaF, ProductoList

urlpatterns = [
    path('clientes/<str:documento>/', ClienteView.as_view(), name='clientes'),
    path('productos/', ProductoView.as_view(), name='productos'),
    path('ListaProductos/', ProductoList.as_view(), name='lista-productos'),
    path('iniciar-venta/', IniciarVentaView.as_view(), name='iniciar-venta'),
    path('APaF/<int:id_producto>/', APaF.as_view(), name='agregar-producto-factura'),
    path('EPaF/<int:id_producto>/', EPaF.as_view(), name='eliminar-producto-factura'),
]
