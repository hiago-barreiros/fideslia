'''
Caso de Uso: Confirmar Pagamento

Confirma um pagamento pendente
'''

from apps.website.models import Pagamentos

class ConfirmarPagamentoDeServico:
    '''
    Serviço responsável por confirmar pagamentos.
    '''

    @staticmethod
    def executar(*, pagamento_id: int) -> Pagamentos:
        '''
        Confirma pagamento pendente.

        Parâmetros:
        - pagamento_id: ID do pagamento

        Retorna: 
        - Pagamento atualizado
        '''

        pagamento = Pagamentos.objects.get(id=pagamento_id)

        # Regra de negócio
        if pagamento.status != 'pendente':
            raise ValueError('Apenas pagamentos podem ser confirmados.')
        
        pagamento.status = 'confirmado'
        pagamento.save()

        return pagamento

