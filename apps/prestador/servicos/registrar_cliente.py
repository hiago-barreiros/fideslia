from apps.website.models import Cliente, PrestadorCliente
from django.core.exceptions import ValidationError

class RegistrarClienteDeServico:

    @staticmethod
    def executar(*, prestador, nome, contato, sexo):
        cliente, criado = Cliente.objects.get_or_create(
            nome=nome,
            contato=contato,
            defaults={'sexo': sexo}
        )

        # prestador não pode duplicar cliente
        if PrestadorCliente.objects.filter(
            prestador=prestador,
            cliente=cliente
        ).exists():
            raise ValidationError(
                'Este cliente já está cadastrado para este prestador.'
            )
        
        PrestadorCliente.objects.create(
            prestador=prestador,
            cliente=cliente
        )

        return cliente

