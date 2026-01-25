# Proposta

## O que é
Representa um orçamento enviado pelo prestador ao cliente.

## Responsabilidade
- Centralizar dados do serviço 
- Valores e estado do orçamento
- Relaciona cliente, itens, aceite e pagamentos

## Relacionamentos
- Pertence a um Prestador
- Pertence a um Cliente
- Possui itens, aceite e pagamentos

- Proposta -> Cliente (muitos para um)
- Proposta -> Prestador (usuário autenticado)

## O que NÃO faz
- Não processa pagamento
- Não autentica cliente
- Não é contrato jurídico

## Estados
- rascunho
- enviada
- visualizada
- aceita
- cancelada
- concluida

## Regras
- Cliente não edita proposta
- Aceite muda estado
- Total é calculado a partir dos itens
