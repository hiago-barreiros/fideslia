### Porque monólito?
Menos complexos, mais fácil de escalar.

### Por que PostgreSQL?
Um dos banco de dados mais usados.

### Por que pagamento não é processado?
Para não fugir do conceito do MVP, tornar o desenvolvimento menos complexos.

### Por que link público?
Para o cliente visualizar.

------

- "Criamos a tabela Cliente como entidade independente para evitar duplicação de dados."

------

### Banco de Dados
Credenciais sensíveis não são versionadas
Configurações carregadas via variáveis de ambiente
.env usado apenas em desenvolvimento

### Por que não armazenar saldo?
O saldo não é armazenado por ser um atributo derivado.
Ele pode ser obtido a qualquer momento a partir da soma dos pagamentos confirmados e do valor total da proposta, evitando inconsistências, problemas de concorrência e erros em estornos.

### Por que permitir múltiplos pagamentos?
O sistema permite múltiplos pagamentos para uma mesma proposta a fim de viabilizar acordos flexíveis entre prestador e cliente, como pagamentos parciais, parcelamentos informais e quitações em etapas, sem perda de histórico financeiro.

### Regra de arredondamento (conceitual)
Valores financeiros devem ser tratados utilizando representação decimal exata.
Cálculos financeiros não devem utilizar ponto flutuante, garantindo precisão, previsibilidade e consistência nos valores armazenados e calculados.

### Por que o status financeiro não é armazenado?
Porque é um estado derivado, calculado dinamicamente a partir dos pagamentos confirmados.

Isso garante:
- Consistência
- Auditabilidade
- Escalabilidade
