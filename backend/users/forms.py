from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = PerfilUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "rut",
            "direccion",
            "comuna",
            "tipo_usuario",
            "password1",
            "password2",
        ]