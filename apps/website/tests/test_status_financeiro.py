from django.test import TestCase
from decimal import Decimal

from django.contrib.auth.models import User
from apps.website.models import Cliente, Proposta, Pagamentos
from apps.website.services.status_financeiro import TestStatusFinanceiroService


class TestStatusFinanceiroService(TestCase):
    """
    Testes do cálculo financeiro da proposta.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="prestador",
            password="123"
        )

        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            contato="31999999999"
        )

        self.proposta = Proposta.objects.create(
            prestador=self.user,
            cliente=self.cliente,
            titulo="Proposta Financeira",
            total=Decimal("100.00")
        )

    def test_proposta_aberta_sem_pagamentos(self):
        """
        Nenhum pagamento confirmado → proposta aberta.
        """

        resultado = TestStatusFinanceiroService.executar(
            proposta_id=self.proposta.id
        )

        self.assertEqual(resultado["status_financeiro"], "aberta")
        self.assertEqual(resultado["total_pago"], Decimal("0.00"))
        self.assertEqual(resultado["saldo"], Decimal("100.00"))

    def test_proposta_em_andamento(self):
        """
        Pagamento parcial confirmado → em andamento.
        """

        Pagamentos.objects.create(
            proposta=self.proposta,
            valor=Decimal("40.00"),
            status="confirmado"
        )

        resultado = TestStatusFinanceiroService.executar(
            proposta_id=self.proposta.id
        )

        self.assertEqual(resultado["status_financeiro"], "em_andamento")
        self.assertEqual(resultado["total_pago"], Decimal("40.00"))
        self.assertEqual(resultado["saldo"], Decimal("60.00"))

