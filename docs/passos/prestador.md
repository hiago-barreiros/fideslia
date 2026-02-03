##Interface do Prestador

### Objetivo
Expor as funcionalidades do sistema ao prestador de serviço por meio de views,
sem duplicar regras de negócio.

### Camadas envolvidas
- Views (Application Layer)
- Serviços (Domain Layer)
- Models (Persistence)

### Funcionalidades
- Dashboard do prestador
- Gestão de propostas
- Registro e confirmação de pagamentos
- Visualização financeira

### Fora do escopo
- Interface do cliente
- APIs externas
- Autenticação avançada

### Decisões arquiteturais
- Views não contêm lógica de negócio
- Serviços são responsáveis por regras e validações
- Histórico financeiro é imutável

