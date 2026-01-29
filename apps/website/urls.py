from django.urls import path
from apps.website.views.pagamento import RegistrarPagamentoView, StatusFinanceiroView

urlpatterns = [
    path('proposta/<int:proposta_id>/pagamento/', RegistrarPagamentoView.as_view()),
    path('proposta/<int:proposta_id>/financeiro/', StatusFinanceiroView.as_view())
]
