from django import forms
from .models import SolicitudArriendo, Inmueble


###########################################################################

                ### FORM INMUEBLE ###

###########################################################################
class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = [
            'nombre',
            'descripcion',
            'm2_construidos',
            'm2_totales',
            'estacionamientos',
            'habitaciones',
            'banos',
            'direccion',
            'precio_mensual',
            'comuna',
            'tipo_inmueble',
            'imagen',
            ]


###########################################################################

                ### FORM SOLICITUD DE ARRIENDO ###

###########################################################################
class SolicitudArriendoForm(forms.ModelForm):
    class Meta:
        model = SolicitudArriendo
        fields = ['inmueble', 'mensaje']