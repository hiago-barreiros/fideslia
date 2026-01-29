from django.urls import path
from .views import index
from apps.website.views.pagamento import (RegistrarPagamentoView, StatusFinanceiroView)

urlpatterns = [
    path('', index, name='index'),
    path('proposta/<int:proposta_id>/pagamentos', RegistrarPagamentoView()),
    path('proposta/<int:proposta_id>/financeiro/', StatusFinanceiroView())
]
