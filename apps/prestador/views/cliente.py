from django.shortcuts import render, redirect
from django.views import View

from apps.prestador.forms.cliente import ClienteForm

class ClienteCreateView(View):

    def get(self, request):
        form = ClienteForm()
        return render(request, 'prestador/cliente_form.html', {'form': form})
    
    def post(self, request):
        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('prestador:dashboard')
        
        return render(request, 'prestador/cliente_form.html', {'form': form})

