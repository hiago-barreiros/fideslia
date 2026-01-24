# Proposta

## O que é
Representa um orçamento enviado pelo prestador ao cliente.

## Responsabilidade
Centralizar dados do serviço, valores e estado do orçamento.

## Relacionamentos
- Pertence a um Prestador
- Pertence a um Cliente
- Possui itens, aceite e pagamentos

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
