from django.contrib import admin
from .models import Cliente, Producto, Factura, DetallesFactura

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id','documento', 'nombre', 'email', 'celular')
    readonly_fields = ('documento',)  

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre', 'precio', 'stock')
    readonly_fields = ('precio',) 

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Producto, ProductoAdmin)

def formato_dinero(valor):
    return "${:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")


class DetallesFacturaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'producto', 'cantidad', 'mostrar_precio_unitario', 'mostrar_precio_total')
    readonly_fields = ('mostrar_precio_unitario', 'mostrar_precio_total')

    def mostrar_precio_unitario(self, obj):
        return formato_dinero(obj.precio_unitario)
    mostrar_precio_unitario.short_description = 'Precio Unitario'

    def mostrar_precio_total(self, obj):
        return formato_dinero(obj.precio_total)
    mostrar_precio_total.short_description = 'Precio Total'

admin.site.register(DetallesFactura, DetallesFacturaAdmin)

class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'cliente', 'vendedor', 'fecha', 'mostrar_total')
    readonly_fields = ('mostrar_total',)

    def mostrar_total(self, obj):
        return formato_dinero(obj.total)
    mostrar_total.short_description = 'Total'
    
admin.site.register(Factura, FacturaAdmin)
