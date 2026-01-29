from django.test import TestCase
from decimal import Decimal


from django.contrib.auth.models import User
from apps.website.models import Cliente, Proposta, Pagamentos
from apps.website.servicos.confirmar_pagamento import ConfirmarPagamentoDeServico

class ConfirmarPagamentoServicoTest(TestCase):
    '''
    Testes do caso de uso: Confirmar Pagamento
    '''

    def setUp(self):
        '''
        Executa antes de cada teste.
        Cria um cenário válido.
        '''

        self.user = User.objects.create_user(
            username='prestador',
            password='123'
        )

        self.cliente = Proposta.objects.create(
            nome='cliente teste',
            contato='33999999999'
        )

        self.proposta = Proposta.objects.create(
            prestador=self.user,
            cliente=self.cliente,
            titulo='Proposta Teste',
            total=Decimal('100.00')
        )

        self.pagamento = Pagamentos.objects.create(
            Proposta=self.proposta,
            valor=Decimal('50.00'),
            status='pendente'
        )

    def test_confirma_pagamento_pendente(self):
        '''
        Deve confirmar um pagamento pendente.
        '''

        pagamento_confirmado = ConfirmarPagamentoDeServico.executar(
            pagamento_id=self.pagamento.id
        )

        self.assertEqual(pagamento_confirmado.status, 'confirmado')


    def test_nao_confirma_pagamento_ja_confirmado(self):
        '''
        Não deve permitir confirmar pagamento já confirmado.
        '''

        self.pagamento.status = 'confirmado'
        self.pagamento.save()

        with self.assertRaises(ValueError):
            ConfirmarPagamentoDeServico.executar(
                pagamento_id=self.pagamento.id
            )

    def test_proposta_quitada(self):
        """
        Total pago igual ao total da proposta → quitada.
        """

        Pagamentos.objects.create(
            proposta=self.proposta,
            valor=Decimal("100.00"),
            status="confirmado"
        )

        resultado = StatusFinanceiroDeServico.executar(
            proposta_id=self.proposta.id
        )

        self.assertEqual(resultado["status_financeiro"], "quitada")
        self.assertEqual(resultado["saldo"], Decimal("0.00"))
