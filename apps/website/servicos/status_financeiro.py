'''
Caso de Uso: Calcular Status financeiro da Proposta

Interpreta a situação financeira da proposta.
'''

from decimal import Decimal
from apps.website.models import Proposta, Pagamento
from django.db.models import Sum

class StatusFinanceiroDeServico:
    '''
    Serviço responsável por calcular o status financeiro de uma proposta.
    '''

    def __init__(self, proposta_id: int):
        self.proposta_id = proposta_id


    def executar(self):
        '''
        Calcula o status financeiro da proposta

        Retorna:
        - total_pago
        - saldo
        - status_financeiro
        '''

        proposta = Proposta.objects.get(id=self.proposta_id)

        pagamentos_confirmados = Pagamento.objects.filter(
            proposta=proposta,
            status='confirmado'
        )

        total_pago = sum(
            (p.valor for p in pagamentos_confirmados),
            Decimal('0.00')
        )

        saldo = proposta.total - total_pago

        if total_pago == Decimal('0.00'):
            status = 'aberta'
        elif total_pago < proposta.total:
            status = 'em_andamento'
        else:
            status = 'quitada'

        return {
            'total_pago': total_pago,
            'saldo': saldo,
            'status_financeiro': status
        }
