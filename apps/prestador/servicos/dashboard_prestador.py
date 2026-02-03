from django.db.models import Sum
from apps.website.models import Proposta, Pagamento

class DashboardPrestadorServico:
    '''
    Consolida dados financeiros e operacionais do prestador.
    '''

    @staticmethod
    def executar():
        propostas = Proposta.objects.all()

        pagamentos = Pagamento.objects.select_related('proposta')

        total_propostas = propostas.count()

        propostas_por_status = {
            'aberta': propostas.filter(status='aberta').count(),
            'aceita': propostas.filter(status='aceita').count(),
            'concluida': propostas.filter(status='concluida').count(),
        }

        tota_recebido = pagamentos.filter(
            status='confirmado'
        ).aggregate(total=Sum('valor'))['total'] or 0

        total_pendente = pagamentos.filter(
            status='pendente'
        ).aggregate(total=Sum('valor'))['total'] or 0

        ultimo_pagamentos = pagamentos.order_by('-id')[:5]

        return {
            'total_propostas': total_propostas,
            'proposta_por_status': propostas_por_status,
            'total_recebido':tota_recebido,
            'total_pendente': total_pendente,
            'ultimos_pagamentos': ultimo_pagamentos,
        }

