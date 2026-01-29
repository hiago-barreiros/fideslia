'''
Caso de Uso: Estornar Pagamento

Remove o efeito financeiro de um pagamento confirmado.
'''

from apps.website.models import Pagamento

'''
Serviço responsável por estornar pagamentos.
'''

@staticmethod
def executar(*, pagamento_id: int) -> Pagamento:
    '''
    Estorna um pagamento confirmado.

    Parâmetros:
    - pagamento_id: ID do pagamento

    Retorna:
    - Pagamento atualizado
    '''

    pagamento = Pagamento.objects.get(id=pagamento_id)

    # Regra de negócio
    if pagamento.status != 'confirmado':
        raise ValueError('Apenas pagamentos confirmados podem ser estornados.')
    
    pagamento.status = 'estornado'
    pagamento.save()

    return pagamento
