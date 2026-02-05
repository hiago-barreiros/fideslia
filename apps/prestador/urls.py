from django.urls import path
from apps.prestador.views.dashboard import dashboard
from apps.prestador.views.cliente import ClienteCreateView

app_name = 'prestador'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('clientes/novo/', ClienteCreateView.as_view(), name='cliente_create'),
]

