from .models import SolicitudArriendo, Inmueble
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView  
from .forms import InmuebleForm, SolicitudArriendoForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages



###########################################################################

                ### CRUD INMUEBLE ###

###########################################################################
class InmuebleCreateView(LoginRequiredMixin, UserPassesTestMixin ,CreateView):
    model = Inmueble
    form_class = InmuebleForm
    template = 'inmueble/inmueble_form.html'
    success_url = 'mis_inmuebles'

    def form_valid(self, form):
        form.instance.propietario = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # Solo permite usuarios tipo ARRENDADOR
        return self.request.user.tipo_usuario == 'ARRENDADOR'



class InmueblePublicListView(ListView):
    model = Inmueble
    template_name = 'web/home.html'
    context_object_name = 'inmuebles'


## LISTAR INMUEBLES DEL USUARIO (SECCION "MI PERFIL")
class MisInmueblesListView(LoginRequiredMixin, ListView):
    model = Inmueble
    template_name = 'inmueble/my_inmueble_list.html'
    context_object_name = 'mis_inmuebles'
    ordering = ["-id"]

    def get_queryset(self):
        return Inmueble.objects.filter(propietario=self.request.user).order_by("-id")
    

## VISTA DE DETALLE DE INMUEBLE 
class InmuebleDetailView(DetailView):
    model = Inmueble
    template_name = 'web/detail.html'


## ACTUALIZAR DATOS INMUEBLE
class InmuebleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = 'inmueble/inmueble_form.html'
    success_url = reverse_lazy('dashboard_arrendador')

    def get_queryset(self):
        return Inmueble.objects.filter(propietario=self.request.user)


## ELIMINAR INMUEBLE
class InmuebleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Inmueble
    template_name = 'inmueble/inmueble_confirm_delete.html'
    success_url = reverse_lazy('dashboard_arrendador')

    def get_queryset(self):
        return Inmueble.objects.filter(propietario=self.request.user)



###########################################################################

                ### CRUD SOLICITUD ARRIENDO ###

###########################################################################

## CREAR SOLICITUD DE ARRIENDO
class SolicitudArriendoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = SolicitudArriendo
    form_class = SolicitudArriendoForm
    template_name = 'solicitud/solicitud_form.html'
    success_url = reverse_lazy('solicitud_list')

    def form_valid(self, form):
        form.instance.arrendatario = self.request.user
        messages.success(self.request, "Solicitud creada correctamente.")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.tipo_usuario == 'ARRENDATARIO'


## LISTAR SOLICITUDES DE ARRIENDO (SECCION "MI PERFIL")
class SolicitudArriendoListView(LoginRequiredMixin, ListView):
    model = SolicitudArriendo
    template_name = 'solicitud/solicitud_list.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        return SolicitudArriendo.objects.filter(arrendatario=self.request.user)


## ACTUALIZAR SOLICITUD DE ARRIENDO
class SolicitudArriendoUpdateView(LoginRequiredMixin, UpdateView):
    model = SolicitudArriendo
    form_class = SolicitudArriendoForm
    template_name = 'solicitud/solicitud_form.html'
    success_url = reverse_lazy('solicitud_list')

    def get_queryset(self):
        return SolicitudArriendo.objects.filter(arrendatario=self.request.user)


## ELIMINAR SOLICITUD DE ARRIENDO
class SolicitudArriendoDeleteView(LoginRequiredMixin, DeleteView):
    model = SolicitudArriendo
    template_name = 'solicitud/solicitud_confirm_delete.html'
    success_url = reverse_lazy('solicitud_list')

    def get_queryset(self):
        return SolicitudArriendo.objects.filter(arrendatario=self.request.user)