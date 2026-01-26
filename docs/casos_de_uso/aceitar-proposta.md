# Aceitar Proposta

## Ator
Cliente

## Descrição
Permite que o cliente aceite formalmente uma proposta.

## Pré-condições
- Proposta deve existir
- Proposta deve estar com status "visualizada"

## Fluxo principal
1. Cliente aceita a proposta
2. Sistema valida o estado atual
3. Sistema altera o status para "aceita"
4. Sistema registra a data de aceite

## Regras de negócio
- Propostas aceitas não podem ser alteradas
- Aceite é irreversível

## Pós-condições
- Proposta pronta para o domínio financeiro
