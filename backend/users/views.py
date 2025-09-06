from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  

            if user.tipo_usuario == 'ARRENDADOR':
                return redirect('dashboard_arrendador')  # URL para arrendadores
            elif user.tipo_usuario == 'ARRENDATARIO':
                return redirect('home')  # URL para arrendatarios
    else:
        form = RegisterForm()
    return render(request, "usuarios/register.html", {"form": form})



def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Has iniciado sesión.")
        if user.tipo_usuario == 'ARRENDADOR':
            return redirect('dashboard_arrendador')  # URL para arrendadores
        elif user.tipo_usuario == 'ARRENDATARIO':
            return redirect('home')  # URL para arrendatarios

    return render(request, "usuarios/login.html", {"form": form})


@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("home")