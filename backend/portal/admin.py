from django.contrib import admin
from .models import Inmueble,SolicitudArriendo

# Register your models here.

@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'propietario', 'comuna', 'tipo_inmueble', 'precio_mensual', 'arrendado', 'creado')
    search_fields = ('nombre', 'descripcion', 'propietario__username', 'comuna__nombre')
    list_filter = ('tipo_inmueble', 'comuna__region', 'arrendado', 'propietario')
    

@admin.register(SolicitudArriendo)
class SolicitudArriendoAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'inmueble', 'arrendatario', 'estado', 'creado')
    search_fields = ('uuid', 'mensaje', 'arrendatario__username', 'inmueble__nombre')
    list_filter = ('estado',)


