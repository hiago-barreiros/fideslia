# Confirmar Pagamento

### Ator
Prestador

### Descrição
Confirma um pagamento pendente, tornando-o válido
para o cálculo financeiro da proposta.

### Pré-condições
- Pagamento deve existir
- Pagamento deve estar com status "pendente"

### Fluxo principal
1. Prestador confirma o pagamento
2. Sistema valida o estado atual
3. Sistema altera o status para "confirmado"

### Regras de negócio
- Apenas pagamentos pendentes podem ser confirmados
- Pagamentos confirmados afetam o total pago
- Confirmação é irreversível

### Pós-condições
- Pagamento considerado no financeiro
