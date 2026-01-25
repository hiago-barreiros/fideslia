# Enviar Proposta

## Ator
Prestador

## Descrição
Permite que o prestador envie uma proposta ao cliente,
alterando seu estado de rascunho para enviada.

## Pré-condições
- Proposta deve existir
- Proposta deve estar em rascunho

## Fluxo principal
1. Prestador solicita envio da proposta
2. Sistema valida o estado atual
3. Sistema altera o status para "enviada"
4. Sistema registra a data de envio

## Regras de negócio
- Propostas enviadas não podem voltar para rascunho
- Proposta só pode ser enviada uma única vez

## Pós-condições
- Proposta disponível para visualização pelo cliente
