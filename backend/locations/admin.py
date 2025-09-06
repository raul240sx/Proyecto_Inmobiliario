from django.contrib import admin
from .models import Region, Comuna

# Register your models here.
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