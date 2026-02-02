from django.contrib import admin
from apps.website.models import Proposta, Pagamento, HistoricoFinanceiro


@admin.register(Proposta)
class PropostaAdmin(admin.ModelAdmin):
    list_display = ('id', 'total', 'status', 'criado_em')
    list_filter = ('status',)
    search_fields = ('id',)


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'proposta', 'valor', 'status', 'criado_em')
    list_filter = ('status',)
    search_fields = ('id',)


@admin.register(HistoricoFinanceiro)
class HistoricoFinanceiroAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'proposta',
        'pagamento',
        'tipo_evento',
        'valor',
        'criado_em',
    )

    list_filter = (
        'tipo_evento',
        'criado_em',
    )

    search_fields = (
        'proposta__id',
        'pagamento__id',
    )

    readonly_fields = (
        'proposta',
        'pagamento',
        'tipo_evento',
        'valor',
        'descricao',
        'criado_em',
    )

    ordering = ('-criado_em',)

    def has_add_permission(self, request):
        '''
        Histórico financeiro NÃO deve ser criado manualmente.
        Apenas via serviços de domínio.
        '''
        return False

    def has_delete_permission(self, request, obj=None):
        '''
        Histórico financeiro é IMUTÁVEL.
        '''
        return False
