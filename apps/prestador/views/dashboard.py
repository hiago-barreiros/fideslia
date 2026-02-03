from django.shortcuts import render
from apps.prestador.servicos.dashboard_prestador import DashboardPrestadorServico

def dashboard(request):
    contexto = DashboardPrestadorServico.executar()
    return render(request, 'prestador/dashboard.html', contexto)


