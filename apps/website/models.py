from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Cliente(models.Model):

    nome = models.CharField(max_length=50)
    contato = models.CharField(max_length=11)
    observacoes = models.TextField(blank=True)

    criando_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Proposta(models.Model):
    
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('enviada', 'Enviada'),
        ('visualizada', 'Visualizada'),
        ('aceita', 'Aceita'),
        ('cancelada', 'Cancelada'),
        ('concluida', 'Concluida'),
    ]

    prestador = models.ForeignKey(
        User,
        on_delete=models.CASCADE, # Se o prestador for removido, remove-se a proposta.
        related_name='proposta'
    )

    cliente = models.ForeignKey(
        'Cliente',
        on_delete=models.PROTECT, # Impede de apagar o cliente se houver propostas.
        related_name='proposta'
    )

    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='rascunho'
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    enviado_em = models.DateTimeField(null=True, blank=True)
    aceito_em = models.DateTimeField(null=True, blank=True)

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def total_pago(self):
        return (
            self.pagamentos.filter(status=Pagamento.STATUS_CONFIRMADO)
            .aggregate(total=sum('valor'))
            .get('total') or 0
        )
    
    def saldo(self):
        return self.total - self.total_pago()
    
    def status_financeiro(self):
        total_pago = self.total_pago()

        if total_pago == 0:
            return 'aberta'
        
        if total_pago < self.total:
            return 'em_andamento'
        
        return 'quitada'

    def __str__(self):
        return f'{self.titulo} - {self.cliente.nome}'

class Pagamento(models.Model):

    STATUS_PENDENTE = 'pendente'
    STATUS_CONFIRMADO = 'confirmado'
    STATUS_CANCELADO = 'cancelado'
    STATUS_ESTORNADO = 'estornado'
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('estornado', 'Estornado')
    ]

    proposta = models.ForeignKey(
        'Proposta',
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
        default='pendente'
    )

    observacoes = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    confirmado_em = models.DateTimeField(null=True, blank=True)

    def confirmar(self):
        '''
        Confirma um pagamento pendente.
        '''

        if self.status != self.STATUS_PENDENTE:
            raise ValidationError('Apenas pagamentos pendentes podem ser confirmados.')
        
        self.status = self.STATUS_CONFIRMADO
        self.confirmado_em = timezone.now()
        self.save()

    def estornar(self):
        '''
        Estorna um pagamento confirmado.
        '''

        if self.status != self.STATUS_CONFIRMADO:
            raise ValidationError('Apenas pagamentos confirmados podem ser estornados.')
        
    def cancelar(self):
        '''
        Cancelar um pagamento pendente.
        '''

        if self.status != self.STATUS_PENDENTE:
            raise ValidationError('Apenas pagamentos pendentes podem ser cancelados.')
        
        self.status = self.STATUS_ESTORNADO
        self.save()

    def __str__(self):
        return f'Pagamento {self.id} - {self.valor}'

class HistoricoFinanceiro(models.Model):
    '''
    Registro imutável de eventos financeiros relacionados a uma proposta.
    '''

    TIPO_EVENTO_CHOICES = [
        ('pagamento_registrado', 'Pagamento registrado'),
        ('pagamento_confirmado', 'Pagamento confirmado'),
        ('pagamento_estornado', 'Pagamento estornado'),
        ('ajuste_manual', 'Ajuste manual'),
    ]

    proposta = models.ForeignKey(
        'website.Proposta',
        on_delete=models.PROTECT,
        related_name='historico_financeiro'
    )

    pagamento = models.ForeignKey(
        'website.Pagamento',
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

    descricao = models.TextField(
        blank=True
    )

    criado_em = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

    class Meta:
        verbose_name = 'Histórico Financeiro'
        verbose_name_plural = 'Históricos Financeiros'
        ordering = ['criado_em']

    def __str__(self):
        return f'{self.proposta} | {self.tipo_evento} | {self.valor}'
    

class HistoricoFianceiro(models.Model):
    proposta = models.ForeignKey(Proposta, on_delete=models.PROTECT)
    pagamento = models.ForeignKey(Pagamento, null=True, blank=True, on_delete=models.PROTECT)
    tipo_evento = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
