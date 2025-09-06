# Documentación del Proyecto - Hito 2

## Requerimiento 1

* Para la creación de un superusuario en la consola se ingresa el comando:

```bash
docker-compose exec web python manage.py createsuperuser
```

* Se rellenan los datos solicitados y finalmente se crea el superusuario.
* La imagen adjunta `creacion_superusuario.png` muestra el proceso en consola.

## Requerimiento 2

* Se registran los modelos en el `admin.py`:

```python
from django.contrib import admin
from .models import Region, Comuna, PerfilUser, Inmueble, SolicitudArriendo

# Register your models here.
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass

@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    pass

@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    pass

@admin.register(SolicitudArriendo)
class SolicitudArriendoAdmin(admin.ModelAdmin):
    pass

@admin.register(PerfilUser)
class PerfilUserAdmin(UserAdmin):
    pass
```

* Con esto se consigue visualizar los modelos en la página del backoffice.

## Requerimiento 3

* Para personalizar la vista del backoffice se agregan:

  * `list_display` para mostrar las columnas con los campos del modelo.
  * `search_fields` para habilitar la barra de búsqueda con los campos correspondientes.
  * `list_filter` para habilitar el cuadro lateral con filtros de búsqueda que dependen de los campos del modelo.
* Adicionalmente, en el modelo `PerfilUser` se agregan `fieldsets` y `add_fieldsets` para mostrar los campos nuevos del usuario modificado.

```python
from django.contrib import admin
from .models import Region, Comuna, PerfilUser, Inmueble, SolicitudArriendo

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'zona')
    search_fields = ('nombre',)
    list_filter = ('zona',)

@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    list_filter = ('region__zona',)

@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'propietario', 'comuna', 'tipo_inmueble', 'precio_mensual', 'arrendado', 'creado')
    search_fields = ('nombre', 'descripcion', 'propietario__username', 'comuna__nombre')
    list_filter = ('tipo_inmueble', 'comuna__region', 'arrendado', 'propietario')

@admin.register(SolicitudArriendo)
class SolicitudArriendoAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'inmueble', 'arrendatario', 'estado', 'creado')
    search_fields = ('uuid', 'mensaje', 'arrendatario__username', 'inmueble__nombre')
    list_filter = ('estado')

@admin.register(PerfilUser)
class PerfilUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'rut', 'is_staff')
    list_filter = ('tipo_usuario', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ("Información extra", {"fields": ("rut", "tipo_usuario")} ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("rut", "tipo_usuario")} ),
    )
```
