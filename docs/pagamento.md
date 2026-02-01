### O que é um pagamento?
Um pagamento é o registro de um valor financeiro recebido pelo prestador, referente a uma proposta, de forma rastreável e historicamente consistente.

### Relacionamento
- Proposta -> Vários Pagamentos
- Pagamentos -> Uma única Proposta
- Cliente -> Não paga diretamente
- Prestador -> É o recebedor

### Regras de negócio
- Total pago = Soma dos pagamentos confirmados
- Saldo = Total da proposta - Total pago
#### Status financeiro da proposta
- Nenhum pagamento = Proposta aberta
- Pagamento parcial = Proposta em andamento

"Proposta aberta" e "em andamento" são status financeiros e independem do status operacioal da proposta.

- Total pago(Total) = Proposta quitada
- Pagamento estornado = Recalcular saldo

------

O Pagamento afeta exclusivamente o domínio financeiro da aplicação.
Ele não altera diretamente o estado operacional da proposta, apenas influencia seu status financeiro.

### Estados
- Pendente
- Confirmado
- Estornado
- Cancelado

Esses estados representam o ciclo de vida financeiro de um pagamento.

### O que acontece quando o estado muda?
- A mudança de estado ocorre conforme a procedência da ação (prestador ou cliente, quando aplicável).
- Cada pagamento segue um fluxo progressivo de estados.
- Estados não podem ser revertidos após a confirmação da transição.
- Um pagamento confirmado pode gerar impacto direto nos cálculos financeiros da proposta.
- Um pagamento estornado implica a reavaliação dos valores financeiros, sem exclusão do registro.

## Caso de uso: Registrar pagamento

Responsável por registrar um pagamento pendente associado a uma proposta.

### Entradas
- ID da proposta
- Valor do pagamento

### Regras
- Pagamento inicia como PENDENTE
- Não altera saldo diretamente
- Não confirma pagamento automaticamente

### Saída
- Entidade Pagamento criada

