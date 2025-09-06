from django.urls import path
from .views import InmueblePublicListView, MisInmueblesListView


urlpatterns = [
    path('', InmueblePublicListView.as_view(), name='home'),
    path('mis_inmuebles/', MisInmueblesListView.as_view(), name='dashboard_arrendador'),
]