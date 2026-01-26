'''
Caso de Uso: Aceitar Proposta

Responsável por registrar o aceite do cliente
'''

from django.utils import timezone
from apps.website.models import Proposta

class AceitarPropostaDeServico:
    '''
    Serviço responsável por aceitar proposta.
    '''

    @staticmethod
    def executar(*, proposta_id: int) -> Proposta:
        '''
        Aceita uma proposta visualizada.

        Parâmetros:
        - proposta_id: ID da proposta

        Retorna:
        - Proposta atualizada
        '''

        proposta = Proposta.objects.get(id=proposta_id)

        # Regra de negócio
        if proposta.status != 'visualizada':
            raise ValueError('A proposta não pode ser aceita neste estado.')
        
        proposta.status = 'aceita'
        proposta.aceito_em = timezone.now()
        proposta.save()

        return proposta

