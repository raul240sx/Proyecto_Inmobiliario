from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Region(models.Model):

    class ZonasDeChile(models.TextChoices):
        norte = "NORTE", _("Zona Norte")
        centro = "CENTRO", _("Zona Centro")
        sur = "SUR", _("Zona Sur")

    zona = models.CharField(max_length=10, choices=ZonasDeChile.choices, null=False, blank=False)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}  | Region: {self.nombre} | Zona: {self.zona}"


class Comuna(models.Model):
    nombre = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="comunas") 

    def __str__(self):
        return f"{self.nombre} | Pertenece a la región: {self.region}"