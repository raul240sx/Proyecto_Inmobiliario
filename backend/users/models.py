from django.db import models
from locations.models import Comuna
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class PerfilUser(AbstractUser):
    class TipoUsuario(models.TextChoices):
        arrendador = "ARRENDADOR", _("Arrendador")
        arrendatario = "ARRENDATARIO", _("Arrendatario")

    rut = models.CharField(max_length=50, unique=True)
    direccion = models.CharField(max_length=100)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=20, choices=TipoUsuario.choices)

    REQUIRED_FIELDS = ['rut', 'email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_username()} | {self.rut}"