from django.http import JsonResponse
from django.views import View

from apps.website.servicos.aceitar_proposta import AceitarPropostaDeServico

# Para o template
from django.shortcuts import render, get_object_or_404
from apps.website.models import Proposta
from apps.website.servicos.status_financeiro import StatusFinanceiroDeServico


class AceitarPropostaView(View):
    '''
    view responsável por aceitar uma proposta.

    IMPORTANTE:
    - Nenhuma regra de negócio aqui
    - Apenas orquestra a requisição
    '''

    def post(self, request, proposta_id):
        try:
            proposta = AceitarPropostaDeServico.executar(
                proposta_id=proposta_id
            )

            return JsonResponse({
                'message': 'Proposta aceita com sucesso',
                'proposta_id': proposta_id,
                'status': proposta.status
            }, status=200)
    
        except ValueError as e:
            return JsonResponse(
                {'error': str(e)},
                status=400
            )


def status_financeiro_proposta(request, proposta_id):
    '''
    Caso de uso: Consultar status financeiro de um proposta.
    '''

    proposta = get_object_or_404(proposta, id=proposta_id)

    status = obter_status_financeiro(proposta)

    contexto = {
        'proposta': proposta,
        'status_financeiro': status['status'],
        'total': status['total'],
        'total_pago': status['total_pago'],
        'saldo': status['saldo']
    }

    return render(request, 'website/proposta_status.html', contexto)
