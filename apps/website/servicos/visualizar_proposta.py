'''
Caso de Uso: Visualizar Proposta
'''

from apps.website.models import Proposta

class VisualizarPropostaDeServico:
    '''
    Serviço responsável por registrar a visualização
    de uma proposta.
    '''

    @staticmethod
    def executar(*, proposta_id: int) -> Proposta:
        '''
        Registra a visualização da proposta.

        Parâmetros:
        - proposta_id: ID da proposta

        Retorna:
        - Proposta
        '''

        proposta = Proposta.objects.get(id=proposta_id)

        # Regra: só propostas enviadas ou já visualizadas podem ser acessadas
        if proposta.status not in ['enviada', 'visualizada']:
            raise ValueError('Proposta não disponivel para visualização.')
        
        # Apenas a primeira visualização altera o estado
        if proposta.status == 'enviada':
            proposta.status = 'visualizada'
            proposta.save()

        return proposta

