'''
Caso de Uso: Calcular Status financeiro da Proposta

Interpreta a situação financeira da proposta.
'''

from decimal import Decimal
from apps.website.models import Proposta, Pagamentos

class StatusFinanceiroDeServico:
    '''
    Serviço responsável por calcular o status financeiro de uma proposta.
    '''

    @staticmethod
    def executar(*, proposta_id: int) -> dict:
        '''
        Calcula o status financeiro da proposta

        Retorna:
        - total_pago
        - saldo
        - status_financeiro
        '''

        proposta = Proposta.objects.get(id=proposta_id)

        pagamentos_confirmados = Pagamentos.objects.filter(
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
