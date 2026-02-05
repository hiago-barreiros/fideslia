from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Sum


class Prestador(models.Model):
    """
    Modelo para prestadores de serviço.
    """
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='prestador'
    )
    
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Prestador'
        verbose_name_plural = 'Prestadores'
    
    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username


class Cliente(models.Model):
    """
    Modelo para clientes.
    """
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro')
    ]

    nome = models.CharField(max_length=100)
    contato = models.CharField(max_length=15)  # Aumentado para suportar formatação
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        blank=True,
        null=True
    )
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)  # Corrigido o typo

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome


class PrestadorCliente(models.Model):
    """
    Relacionamento entre prestadores e clientes.
    """
    prestador = models.ForeignKey(
        Prestador,
        on_delete=models.CASCADE,
        related_name='vinculos_clientes'  # Mais descritivo
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='vinculos_prestadores'  # Mais descritivo
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('prestador', 'cliente')
        verbose_name = 'Vínculo Prestador-Cliente'
        verbose_name_plural = 'Vínculos Prestador-Cliente'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.prestador} - {self.cliente}'


class Proposta(models.Model):
    """
    Proposta de serviço enviada pelo prestador ao cliente.
    """
    STATUS_RASCUNHO = 'rascunho'
    STATUS_ENVIADA = 'enviada'
    STATUS_VISUALIZADA = 'visualizada'
    STATUS_ACEITA = 'aceita'
    STATUS_CANCELADA = 'cancelada'
    STATUS_CONCLUIDA = 'concluida'
    
    STATUS_CHOICES = [
        (STATUS_RASCUNHO, 'Rascunho'),
        (STATUS_ENVIADA, 'Enviada'),
        (STATUS_VISUALIZADA, 'Visualizada'),
        (STATUS_ACEITA, 'Aceita'),
        (STATUS_CANCELADA, 'Cancelada'),
        (STATUS_CONCLUIDA, 'Concluída'),
    ]

    prestador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='propostas'  # Plural consistente
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='propostas'  # Plural consistente
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_RASCUNHO
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    enviado_em = models.DateTimeField(null=True, blank=True)
    aceito_em = models.DateTimeField(null=True, blank=True)
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    class Meta:
        verbose_name = 'Proposta'
        verbose_name_plural = 'Propostas'
        ordering = ['-criado_em']

    def total_pago(self):
        """Retorna o total de pagamentos confirmados."""
        total = self.pagamentos.filter(
            status=Pagamento.STATUS_CONFIRMADO
        ).aggregate(total=Sum('valor'))['total']
        return total or 0
    
    def saldo(self):
        """Retorna o saldo restante a pagar."""
        return self.total - self.total_pago()
    
    def status_financeiro(self):
        """Retorna o status financeiro da proposta."""
        total_pago = self.total_pago()

        if total_pago == 0:
            return 'aberta'
        elif total_pago < self.total:
            return 'em_andamento'
        else:
            return 'quitada'

    def __str__(self):
        return f'{self.titulo} - {self.cliente.nome}'


class Pagamento(models.Model):
    """
    Pagamento relacionado a uma proposta.
    """
    STATUS_PENDENTE = 'pendente'
    STATUS_CONFIRMADO = 'confirmado'
    STATUS_CANCELADO = 'cancelado'
    STATUS_ESTORNADO = 'estornado'
    
    STATUS_CHOICES = [
        (STATUS_PENDENTE, 'Pendente'),
        (STATUS_CONFIRMADO, 'Confirmado'),
        (STATUS_CANCELADO, 'Cancelado'),
        (STATUS_ESTORNADO, 'Estornado')
    ]

    proposta = models.ForeignKey(
        Proposta,
        on_delete=models.CASCADE,
        related_name='pagamentos'
    )
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDENTE
    )
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    confirmado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-criado_em']

    def confirmar(self):
        """Confirma um pagamento pendente."""
        if self.status != self.STATUS_PENDENTE:
            raise ValidationError('Apenas pagamentos pendentes podem ser confirmados.')
        
        self.status = self.STATUS_CONFIRMADO
        self.confirmado_em = timezone.now()
        self.save()

    def estornar(self):
        """Estorna um pagamento confirmado."""
        if self.status != self.STATUS_CONFIRMADO:
            raise ValidationError('Apenas pagamentos confirmados podem ser estornados.')
        
        self.status = self.STATUS_ESTORNADO
        self.confirmado_em = None  # Remove a data de confirmação
        self.save()

    def cancelar(self):
        """Cancela um pagamento pendente."""
        if self.status != self.STATUS_PENDENTE:
            raise ValidationError('Apenas pagamentos pendentes podem ser cancelados.')
        
        self.status = self.STATUS_CANCELADO
        self.save()

    def __str__(self):
        return f'Pagamento #{self.id} - R$ {self.valor}'


class HistoricoFinanceiro(models.Model):
    """
    Registro imutável de eventos financeiros relacionados a uma proposta.
    """
    TIPO_PAGAMENTO_REGISTRADO = 'pagamento_registrado'
    TIPO_PAGAMENTO_CONFIRMADO = 'pagamento_confirmado'
    TIPO_PAGAMENTO_ESTORNADO = 'pagamento_estornado'
    TIPO_AJUSTE_MANUAL = 'ajuste_manual'
    
    TIPO_EVENTO_CHOICES = [
        (TIPO_PAGAMENTO_REGISTRADO, 'Pagamento registrado'),
        (TIPO_PAGAMENTO_CONFIRMADO, 'Pagamento confirmado'),
        (TIPO_PAGAMENTO_ESTORNADO, 'Pagamento estornado'),
        (TIPO_AJUSTE_MANUAL, 'Ajuste manual'),
    ]

    proposta = models.ForeignKey(
        Proposta,
        on_delete=models.PROTECT,
        related_name='historico_financeiro'
    )
    pagamento = models.ForeignKey(
        Pagamento,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='historicos'
    )
    tipo_evento = models.CharField(
        max_length=50,
        choices=TIPO_EVENTO_CHOICES
    )
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

    class Meta:
        verbose_name = 'Histórico Financeiro'
        verbose_name_plural = 'Históricos Financeiros'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.proposta} | {self.get_tipo_evento_display()} | R$ {self.valor}'