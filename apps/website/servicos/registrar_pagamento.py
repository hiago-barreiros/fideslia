'''
Caso de Uso: Registra Pagamento

Cria um pagamento vinculado a um proposta aceita.
'''

from apps.website.models import Proposta, Pagamento
from apps.website.servicos.registrar_evento_financeiro import RegistrarEventoFinanceiroDeServico

class RegistrarPagamentoDeServico:
    '''
    Serviço responsável por registrar pagamentos.
    '''

    @staticmethod
    def executar(*, proposta_id: int, valor) -> Pagamento:
        '''
        Registra um pagamento pendente

        Parâmetros:
        - proposta_id: ID da proposta
        - valor: valor do pagamento

        Retorna:
        - Pagamento criado
        '''

        # O pagamento não existe sem proposta.
        proposta = Proposta.objects.get(id=proposta_id)

        # Regra de negócio
        if proposta.status != 'aceita':
            raise ValueError('Pagamentos só podem ser registrados para propostas aceitas.')
        
        pagamento = Pagamento.objects.create(
            proposta=proposta,
            valor=valor,
            status='pendente'
        )

        # 🔹 Histórico financeiro
        RegistrarEventoFinanceiroDeServico(
            proposta=pagamento.proposta,
            pagamento=pagamento,
            tipo_evento='pagamento_registrado',
            valor=valor,
            descricao='Pagamento registrado'
        ).executar()


        return pagamento
