from django.urls import path
from apps.website.views import home


# Views - Proposta
from apps.website.views.proposta import status_financeiro_proposta

# Views - Pagamento
from apps.website.views.pagamento import (RegistrarPagamentoView, StatusFinanceiroView, ConfirmarPagamentoView, EstornarPagamentoView)

urlpatterns = [

    path('', home, name='home'),

    # PROPOSTA
    path('proposta/<int:proposta_id>/financeiro/', StatusFinanceiroView.as_view(), name='financeiro_proposta'),
    path("proposta/<int:proposta_id>/status-financeiro/", status_financeiro_proposta, name="status_financeiro"),

    # PAGAMENTO
    path('proposta/<int:proposta_id>/pagamento/', RegistrarPagamentoView.as_view(), name='registrar_pagamento'),
    path('pagamento/<int:pagamento_id>/confirmar/', ConfirmarPagamentoView.as_view(), name='confirmar_pagamento'),
    path('pagamento/<int:pagamento_id>/estornar/', EstornarPagamentoView.as_view(), name='estornar_pagamento'),
]

