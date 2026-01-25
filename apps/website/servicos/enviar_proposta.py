'''
Caso de Uso: Enviar proposta

Responsável por válidar e executar a transição
de estado da proposta de rascunho para enviada
'''

from django.utils import timezone
from apps.website.models import Proposta

class EnviarPropostaDeServico:
    '''
    Serviço responsável por enviar proposta
    '''

    @staticmethod
    def executar(*, proposta_id: int) -> Proposta:
        '''
        Enviar uma proposta, caso esteja em rascunho

        Parâmetros: 
        - proposta_id: ID da proposta a ser enviada

        Retorna:
        - Proposta atualizada

        Lança: 
        - ValueError ser a proposta não puder ser enviada
        '''

        proposta = Proposta.objects.get(id=proposta_id)

        # Regra de negócio: só pode enviar se estiver em rascunho
        if proposta.status != 'rascunho':
            raise ValueError('A proposta não pode ser enviada neste estado.')
        
        proposta.status = 'enviada'
        proposta.enviada_em = timezone.now()

        proposta.save()

        return proposta
