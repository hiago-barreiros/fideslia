'''
Caso de uso: Criar Proposta

Responsável por encapsular toda a regra de criação
de uma proposta, sem depender de views ou HTTP.
'''

from apps.website.models import Proposta, Cliente
from django.contrib.auth.models import User

class CriarPropostaDeServico:
    '''
    Serviço de aplicação responsável por criar proposta
    '''

    @staticmethod
    def executar(*, prestador: User, cliente_id: int, titulo: str, descricao: str = "") -> Proposta:
        '''
        Cria uma nova proposta no estado inicial (rascunho).

        Parâmetros:
        - prestador: usuário responsável pela proposta
        - cliente_id: ID do cliente vinculo
        - titulo: título da proposta
        - descrição: descrição opcional

        Retorna:
        - Objeto Proposta criado
        '''

        # Busca o cliente no banco
        cliente = Cliente.objects.get(id=cliente_id)

        # Cria a proposta respeitando as regras de negócio
        proposta = Proposta.objects.create(
            prestador = prestador,
            cliente = cliente,
            titulo = titulo,
            descricao = descricao,
            status = 'rascunho',
            total = 0
        )

        return proposta


