import json
from django.http import JsonResponse
from django.views import View

from apps.website.servicos.registrar_pagamento import RegistrarPagamentoDeServico
from apps.website.servicos.status_financeiro import StatusFinanceiroDeServico

class RegistrarPagamentoView(View):
    '''
    Registra um pagamento pendente.
    '''

    def post(self, request, proposta_id):
        data = json.loads(request.body)

        try:
            pagamento = RegistrarPagamentoDeServico.executar(
                proposta_id=proposta_id,
                valor=data['valor']
            )

            return JsonResponse({
                "message": "Pagamento registrado",
                "pagamento_id": pagamento.id,
                "status": pagamento.status
            }, status=201)

        except ValueError as e:
            return JsonResponse(
                {"error": str(e)},
                status=400
            )

class StatusFinanceiroView(View):
    '''
    Retorna o status financceiro de uma proposta.
    Não altera estado, apenas calcula
    '''
    def get(self, request, proposta_id):
        resultado = StatusFinanceiroDeServico.executar(
            proposta_id=proposta_id
        )

        return JsonResponse(resultado, status=200)
