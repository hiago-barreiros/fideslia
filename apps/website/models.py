from django.db import models
from djando.contrib.auth.models import User

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

    def __str__(self):
        return f'{self.titulo} - {self.cliente.nome}'


