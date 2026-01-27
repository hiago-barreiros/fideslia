# Registrar Pagamento

### Ator
Prestador

### Descrição
Permite registrar um pagamento vinculado a uma proposta aceita.

### Pré-condições
- Proposta deve existir
- Proposta deve estar com status "aceita"

### Fluxo principal
1. Prestador registra um pagamento
2. Sistema cria o pagamento como "pendente"
3. Pagamento não altera o status operacional da proposta

### Regras de negócio
- Propostas não aceitas não podem receber pagamentos
- Apenas pagamentos confirmados afetam o total pago
- Saldo é um valor calculado, não armazenado

### Pós-condições
- Pagamento registrado no sistema
