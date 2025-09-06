from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PerfilUser

# Register your models here.

@admin.register(PerfilUser)
class PerfilUserAdmin(UserAdmin): 
    list_display = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'rut', 'is_staff')
    list_filter = ('tipo_usuario', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'rut')
    
    fieldsets = UserAdmin.fieldsets + (
        ("Información extra", {"fields": ("rut", "tipo_usuario")}),
        )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("rut", "tipo_usuario")}),
        )