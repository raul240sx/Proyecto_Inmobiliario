from django.db import models
from locations.models import Comuna
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import uuid

# Create your models here.


class Inmueble(models.Model):

    class TipoInmueble(models.TextChoices):
        casa = "CASA", _("Casa")
        departamento = "DEPARTAMENTO", _("Departamento")
        parcela = "PARCELA", _("Parcela")

    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inmuebles", blank=True, null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    m2_construidos = models.FloatField(default=0)
    m2_totales = models.FloatField(default=0)
    estacionamientos = models.PositiveIntegerField(default=0)
    habitaciones = models.PositiveIntegerField(default=0)
    banos = models.PositiveIntegerField(default=0)
    direccion = models.CharField(max_length=100)
    precio_mensual = models.DecimalField(max_digits=8, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    actualizado = models.DateTimeField(auto_now=True, blank=True, null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    tipo_inmueble = models.CharField(max_length=20, choices=TipoInmueble.choices)
    imagen = models.ImageField(upload_to='imagenes_inmueble/', default='imagenes_inmueble/casa-sin-imagen')
    arrendado = models.BooleanField(default=False)



class SolicitudArriendo(models.Model):

    class EstadoSolicitud(models.TextChoices):
        pendiente = "PENDIENTE", _("Pendiente")
        aprobada = "APROBADA", _("Aprobada")
        rechazada = "RECHAZADA", _("Rechazada")

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name="solicitudes")
    mensaje = models.TextField()
    arrendatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solicitudes_enviadas')
    estado = models.CharField(max_length=20, choices=EstadoSolicitud.choices, default=EstadoSolicitud.pendiente)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.uuid} | Persona que solicita: {self.arrendatario} | Estado solicitud: {self.estado} "