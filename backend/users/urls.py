from django.urls import path
from .views import register_view, login_view, logout_view


urlpatterns = [
    path('registro/', register_view, name='register'),
    path('ingresar/', login_view, name='login'),
    path("logout/", logout_view, name="logout"),

]