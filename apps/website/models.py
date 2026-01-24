from django.db import models

class Cliente(models.Model):

    nome = models.CharField(max_length=50)
    contato = models.CharField(max_length=11)
    observacoes = models.TextField(blank=True)

    criando_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
