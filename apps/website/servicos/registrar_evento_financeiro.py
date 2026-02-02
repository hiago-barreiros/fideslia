'''
Caso de Uso: Registrar Evento Financeiro

Responsável por registrar qualquer movimentação financeira
da proposta (pagamentos, estornos, ajustes, etc.)
'''

from django.core.exceptions import ValidationError

from apps.website.models import HistoricoFinanceiro


class RegistrarEventoFinanceiroDeServico:
    '''
    Serviço central de registro financeiro (AUDIT LOG)
    '''

    def __init__(
        self,
        *,
        proposta,
        tipo_evento,
        valor,
        pagamento=None,
        descricao=''
    ):
        self.proposta = proposta
        self.pagamento = pagamento
        self.tipo_evento = tipo_evento
        self.valor = valor
        self.descricao = descricao

    def executar(self):
        '''
        Registra evento financeiro imutável
        '''

        # 🔒 Validações mínimas
        if self.valor == 0:
            raise ValidationError('Evento financeiro não pode ter valor zero.')

        if not self.tipo_evento:
            raise ValidationError('Tipo de evento financeiro é obrigatório.')

        historico = HistoricoFinanceiro.objects.create(
            proposta=self.proposta,
            pagamento=self.pagamento,
            tipo_evento=self.tipo_evento,
            valor=self.valor,
            descricao=self.descricao
        )

        return historico




