import json
from django.http import JsonResponse, Http404
from django.views import View
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.website.models import Pagamento
from apps.website.servicos.registrar_pagamento import RegistrarPagamentoDeServico
from apps.website.servicos.status_financeiro import StatusFinanceiroDeServico
from apps.website.servicos.confirmar_pagamento import ConfirmarPagamentoDeServico
from apps.website.servicos.estornar_pagamento import EstornarPagamentosDeServico

class ConfirmarPagamentoView(View):
    '''
    Confirma um pagamento existente.
    '''

    def post(self, request, pagamento_id):
        try:
            servico = ConfirmarPagamentoDeServico(pagamento_id)
            pagamento = servico.executar()

            return JsonResponse({
                'mensagem': 'Pagamento confirmado com sucesso',
                'pagamento_id': pagamento.id,
                'status': pagamento.status
            })
    
        except Pagamento.DoesNotExist:
            raise Http404('Pagamento não encontrado.')
        
        except ValidationError as e:
            return JsonResponse(
                {'error': str(e)},
                status=400
            )


class RegistrarPagamentoView(View):
    '''
    Registra um pagamento pendente.
    '''

    def post(self, request, proposta_id):


        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'JSON inválido.'},
                status=400
            )
        
        try:
            servico = RegistrarPagamentoDeServico(
                proposta_id=proposta_id,
                valor=data['valor']
            )
            pagamento = servico.executar()

            return JsonResponse({
                'message': 'Pagamento registrado com sucesso',
                'pagamento_id': pagamento.id,
                'status': pagamento.status
            }, status=201)
        
        except (KeyError, ValueError) as e:
            return JsonResponse(
                {'error': str(e)},
                status=400
            )


class StatusFinanceiroView(View):
    '''
    Retorna o status financceiro de uma proposta.
    Não altera estado, apenas calcula
    '''
    def get(self, request, proposta_id):
            servico = StatusFinanceiroDeServico(proposta_id)
            resultado = servico.executar()

            return JsonResponse(resultado, status=200)
    

class EstornarPagamentoView(View):

    def post(self,request, pagamento_id):
        try:
            servico = EstornarPagamentosDeServico(pagamento_id)
            pagamento = servico.executar()

            return JsonResponse({
                'message': 'Pagamento estornado com sucesso',
                'pagamento_id': pagamento_id,
                'status': pagamento.status
            })
        
        except ValidationError as e:
            return JsonResponse(
                {'error': str(e)},
                status=400
            )

    def get(self, request, proposta_id):
        servico = StatusFinanceiroDeServico(proposta_id)
        data = servico.executar()

        return JsonResponse(data)