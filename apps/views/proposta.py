from django.http import JsonResponse
from django.views import View

from apps.website.servicos.aceitar_proposta import AceitarPropostaDeServico

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

