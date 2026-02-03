from django.urls import path
from apps.prestador.views.dashboard import dashboard

app_name = 'prestador'

urlpatterns = [
    path('', dashboard, name='prestador_dashboard'),
]

