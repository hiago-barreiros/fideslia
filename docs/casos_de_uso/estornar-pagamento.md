# Estornar Pagamento

### Ator
Prestador

### Descrição
Remove o efeito financeiro de um pagamento confirmado,
sem apagar o registro.

### Pré-condições
- Pagamento deve existir
- Pagamento deve estar com status "confirmado"

### Fluxo principal
1. Prestador solicita o estorno
2. Sistema valida o estado atual
3. Sistema altera o status para "estornado"

### Regras de negócio
- Apenas pagamentos confirmados podem ser estornados
- Estorno é irreversível
- Pagamentos estornados não afetam o financeiro

### Pós-condições
- Saldo da proposta passa a ser recalculado
