## Organização de Views

Quando um app possuir múltiplas views organizadas por contexto
(dashboard, proposta, pagamento, etc), deve-se usar:

apps/<app>/views/

Regra obrigatória:
- A pasta `views/` deve conter um arquivo `__init__.py`

Exemplo válido:
apps/prestador/views/dashboard.py
