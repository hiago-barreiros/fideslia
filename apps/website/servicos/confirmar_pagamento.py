'''
Caso de Uso: Confirmar Pagamento

Confirma um pagamento pendente
'''

from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.website.models import Pagamento
from apps.website.servicos.status_financeiro import StatusFinanceiroDeServico

class ConfirmarPagamentoDeServico:
    '''
    Serviço responsável por confirmar pagamentos.
    '''

    def __init__(self, pagamento_id):
        self.pagamento_id = pagamento_id


    def executar(self):
        '''
        Confirma pagamento pendente.

        Parâmetros:
        - pagamento_id: ID do pagamento

        Retorna: 
        - Pagamento atualizado
        '''

        pagamento = Pagamento.objects.select_related('proposta').get(id=self.pagamento_id)

        # Regra de negócio
        if pagamento.status == 'confirmado':
            raise ValidationError('Pagamento já está confirmado.')

        if pagamento.status != 'pendente':
            raise ValueError('Apenas pagamentos podem ser confirmados.')
    

        pagamento.status = 'confirmado'
        pagamento.confirmado_em = timezone.now()
        pagamento.save()

        # 🔹 Recalcula status financeiro da proposta
        status_financeiro = StatusFinanceiroDeServico(pagamento.proposta.id).executar()

        # 🔹 Atualiza status da proposta se estiver quitada
        if status_financeiro['status_financeiro'] == 'quitada':
            proposta = pagamento.proposta
            proposta.status = 'concluida'
            proposta.aceito_em = timezone.now()
            proposta.save()

        return pagamento

