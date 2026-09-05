# GreenUp Backend

API REST do Projeto Integrador GreenUp, implementada com Django, Django REST Framework, JWT e PostgreSQL.

## Execução com Docker

1. Copie `.env.example` para `.env` e altere os segredos.
2. Execute `docker compose up --build`.
3. Crie um administrador com `docker compose exec api python manage.py createsuperuser`.
4. A API ficará disponível em `http://localhost:8000/api/v1/`.

## Execução local para desenvolvimento

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

O PostgreSQL é o banco padrão. A variável `USE_SQLITE=True` existe apenas para testes automatizados isolados.

## Regras implementadas

- RNE-001: somente usuário autenticado registra descarte.
- RNE-002: código da lixeira, categoria, quantidade, itens, foto e nível 1-4 são obrigatórios.
- RNE-003: a passagem do nível 1-3 para o nível 4 gera notificação ao gestor.
- RNE-004: administradores podem suspender e reativar usuários.
- Cada item descartado gera 10 pontos, calculados no serviço de descarte.
- Histórico pessoal nunca retorna descartes de outro usuário.
- Entidades operacionais importantes usam exclusão lógica.

## Testes

```bash
USE_SQLITE=True python manage.py test
```
