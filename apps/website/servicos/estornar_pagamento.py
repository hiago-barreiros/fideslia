'''
Caso de Uso: Estornar Pagamento

Remove o efeito financeiro de um pagamento confirmado.
'''
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.website.models import Pagamento
from apps.website.servicos.status_financeiro import StatusFinanceiroDeServico
from apps.website.servicos.registrar_evento_financeiro import RegistrarEventoFinanceiroDeServico

'''
Serviço responsável por estornar pagamentos.
'''

class EstornarPagamentosDeServico:

    def __int__(self, pagamento_id):
        self.pagamento_id = pagamento_id

    def executar(self):
        '''
        Estorna um pagamento confirmado.

        Parâmetros:
        - pagamento_id: ID do pagamento

        Retorna:
        - Pagamento atualizado
        '''

        pagamento = Pagamento.objects.select_related('proposta').get(id=self.pagamento_id)

        # Regra de negócio
        if pagamento.status != 'confirmado':
            raise ValueError('Apenas pagamentos confirmados podem ser estornados.')
        
        if pagamento.status == 'pendente':
            raise ValidationError('Pagamento pendente não pode ser estornado.')
        
        if pagamento.status == 'estornado':
            raise ValidationError('Pagamento já foi estornado.')
        
        pagamento.status = 'estornado'
        pagamento.estornar()
        pagamento.save()

        # Recalcula status financeiro
        status_financeiro = StatusFinanceiroDeServico(pagamento.proposta.id).executar()
        proposta = pagamento.proposta

        # Se não estiver mais quitada, volta status
        if status_financeiro['status_financeiro'] != 'quitada':
            proposta.status = 'aceita'
            proposta.save()

        RegistrarEventoFinanceiroDeServico(
            proposta=pagamento.proposta,
            pagamento=pagamento,
            tipo_evento='pagamento_estornado',
            valor=-pagamento.valor,
            descricao='Pagamento estornado'
        ).executar()

        return pagamento
