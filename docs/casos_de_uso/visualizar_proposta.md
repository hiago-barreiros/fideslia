# Visualizar Proposta

### Ator
Cliente

### Descrição
Registra a visualização de uma proposta enviada.

### Pré-condições
- Proposta deve existir
- Proposta deve estar com status "enviada" ou "visualizada"

### Fluxo principal
1. Cliente acessa o link da proposta
2. Sistema registra a visualização
3. Caso seja a primeira visualização, o status é atualizado

### Regras de negócio
- Proposta só muda para "visualizada" uma única vez
- Visualizações repetidas não alteram o estado

### Pós-condições
- Proposta marcada como visualizada
