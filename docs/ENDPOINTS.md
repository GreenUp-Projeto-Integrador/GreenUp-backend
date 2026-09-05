# Endpoints da API GreenUp

Base da API: `/api/v1`

Todas as rotas protegidas exigem o cabeçalho de autenticação HTTP com token JWT:
```http
Authorization: Bearer <access_token>
```

Em caso de erro de validação ou de negócio, a API retorna a estrutura padronizada:
```json
{
  "success": false,
  "error": {
    "status": 400,
    "message": "Não foi possível concluir a operação.",
    "fields": {
      "campo": ["Descrição do erro."]
    }
  }
}
```

---

## Tabela Geral de Rotas

| Método | Endpoint | Acesso | Responsabilidade |
|---|---|---|---|
| POST | `/auth/register/` | Público | Cadastrar usuário comum |
| POST | `/auth/token/` | Público | Obter access e refresh token JWT |
| POST | `/auth/token/refresh/` | Público | Renovar o token de acesso |
| GET | `/users/me/` | Autenticado | Consultar os próprios dados de perfil |
| PATCH | `/users/me/` | Autenticado | Editar parcialmente os próprios dados |
| POST | `/users/me/change-password/` | Autenticado | Alterar a senha com validação da senha atual |
| GET | `/users/me/summary/` | Autenticado | Consultar pontos, nível e quantidade de descartes |
| POST | `/users/{id}/suspend/` | Administrador | Suspender uma conta de usuário |
| POST | `/users/{id}/reactivate/` | Administrador | Reativar uma conta de usuário |
| GET/POST | `/collection-points/` | Público (GET) / Gestor ou Admin (POST) | Listar pontos de coleta ativos ou cadastrar novo ponto |
| GET | `/collection-points/{id}/` | Público | Consultar detalhes de um ponto e suas lixeiras |
| GET/POST | `/collection-points/{id}/trash-bins/` | Público (GET) / Gestor ou Admin (POST) | Listar ou cadastrar lixeiras de um ponto de coleta específico |
| GET/POST | `/collection-points/trash-bins/` | Autenticado (GET) / Gestor ou Admin (POST) | Listar todas as lixeiras ativas ou cadastrar lixeira |
| GET/PATCH/PUT | `/collection-points/trash-bins/{id}/` | Autenticado (GET) / Gestor ou Admin (PATCH/PUT) | Consultar ou atualizar dados de uma lixeira (sem exclusão) |
| GET | `/collection-points/trash-bins/by-code/{code}/` | Autenticado | Validar e consultar lixeira por código/QR Code |
| GET | `/disposals/` | Autenticado | Listar histórico paginado de descartes do usuário |
| POST | `/disposals/` | Autenticado | Registrar novo descarte com upload de imagem |
| GET | `/disposals/categories/` | Público | Listar todas as categorias de resíduos |
| GET | `/disposals/{id}/` | Proprietário | Consultar detalhes de um descarte próprio |
| GET | `/ranking/` | Público | Consultar o ranking dos 100 maiores pontuadores |
| GET | `/notifications/` | Gestor / Admin | Listar notificações do gestor autenticado |
| PATCH | `/notifications/{id}/read/` | Destinatário | Marcar notificação como lida |
| GET | `/dashboard/statistics/` | Autenticado | Obter estatísticas agregadas de descartes por período |

---

## 1. Autenticação (`/auth`)

### 1.1. Cadastrar Usuário
- **Método:** `POST`
- **Endpoint:** `/api/v1/auth/register/`
- **Acesso:** Público
- **Headers:** `Content-Type: application/json`
- **Payload esperado:**
```json
{
  "name": "João Silva",
  "email": "joao.silva@example.com",
  "password": "SenhaForte123!",
  "confirmPassword": "SenhaForte123!"
}
```
- **Resposta (`201 Created`):**
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao.silva@example.com"
}
```

---

### 1.2. Obter Tokens JWT (Login)
- **Método:** `POST`
- **Endpoint:** `/api/v1/auth/token/`
- **Acesso:** Público
- **Headers:** `Content-Type: application/json`
- **Payload esperado:**
```json
{
  "email": "joao.silva@example.com",
  "password": "SenhaForte123!"
}
```
- **Resposta (`200 OK`):**
```json
{
  "refresh": "eyJhbGciOi...",
  "access": "eyJhbGciOi..."
}
```

---

### 1.3. Renovar Token de Acesso
- **Método:** `POST`
- **Endpoint:** `/api/v1/auth/token/refresh/`
- **Acesso:** Público
- **Headers:** `Content-Type: application/json`
- **Payload esperado:**
```json
{
  "refresh": "eyJhbGciOi..."
}
```
- **Resposta (`200 OK`):**
```json
{
  "access": "eyJhbGciOi..."
}
```

---

## 2. Usuários e Perfil (`/users`)

### 2.1. Consultar Próprio Perfil
- **Método:** `GET`
- **Endpoint:** `/api/v1/users/me/`
- **Acesso:** Autenticado
- **Parâmetros de pesquisa (Query Params):** Nenhum
- **Resposta (`200 OK`):**
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao.silva@example.com",
  "phone": "11999999999",
  "cpf": "123.456.789-00",
  "address": "Av. Brasil, 1500",
  "city": "São Paulo",
  "state": "SP",
  "zipCode": "01310-100",
  "role": "USER"
}
```

---

### 2.2. Atualizar Próprio Perfil
- **Método:** `PATCH`
- **Endpoint:** `/api/v1/users/me/`
- **Acesso:** Autenticado
- **Headers:** `Content-Type: application/json`
- **Payload esperado (campos opcionais):**
```json
{
  "name": "João Silva Santos",
  "phone": "11988888888",
  "cpf": "123.456.789-00",
  "address": "Rua das Palmeiras, 45",
  "city": "São Paulo",
  "state": "SP",
  "zipCode": "01310-200"
}
```
- **Resposta (`200 OK`):** Retorna o objeto do perfil atualizado.

---

### 2.3. Alterar Senha
- **Método:** `POST`
- **Endpoint:** `/api/v1/users/me/change-password/`
- **Acesso:** Autenticado
- **Headers:** `Content-Type: application/json`
- **Payload esperado:**
```json
{
  "currentPassword": "SenhaAntiga123!",
  "newPassword": "NovaSenhaForte123!",
  "confirmPassword": "NovaSenhaForte123!"
}
```
- **Resposta (`200 OK`):**
```json
{
  "success": true,
  "message": "Senha alterada com sucesso."
}
```

---

### 2.4. Resumo da Conta (Pontos e Nível)
- **Método:** `GET`
- **Endpoint:** `/api/v1/users/me/summary/`
- **Acesso:** Autenticado
- **Parâmetros de pesquisa (Query Params):** Nenhum
- **Resposta (`200 OK`):**
```json
{
  "name": "João Silva",
  "email": "joao.silva@example.com",
  "joinDate": "2026-09-03",
  "points": 120,
  "level": "Bronze",
  "disposalsCount": 6
}
```

---

### 2.5. Suspender Usuário
- **Método:** `POST`
- **Endpoint:** `/api/v1/users/{id}/suspend/`
- **Acesso:** Administrador (`role == ADMIN`)
- **Parâmetros de Path:**
  - `id` *(int)*: ID do usuário a ser suspenso.
- **Payload esperado:** Nenhum (corpo da requisição vazio)
- **Resposta (`204 No Content`):** Corpo vazio.

---

### 2.6. Reativar Usuário
- **Método:** `POST`
- **Endpoint:** `/api/v1/users/{id}/reactivate/`
- **Acesso:** Administrador (`role == ADMIN`)
- **Parâmetros de Path:**
  - `id` *(int)*: ID do usuário a ser reativado.
- **Payload esperado:** Nenhum (corpo da requisição vazio)
- **Resposta (`204 No Content`):** Corpo vazio.

---

## 3. Pontos de Coleta e Lixeiras (`/collection-points`)

### 3.1. Listar Pontos de Coleta
- **Método:** `GET`
- **Endpoint:** `/api/v1/collection-points/`
- **Acesso:** Público
- **Parâmetros de pesquisa (Query Params):**
  - `page` *(opcional, int)*: Número da página (paginação padrão de 20 itens por página). Exemplo: `?page=1`
- **Resposta (`200 OK`):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Campus Principal",
      "address": "Av. Universitária, 100",
      "latitude": "-16.328000",
      "longitude": "-48.953000",
      "trashBins": [
        {
          "id": 1,
          "code": "A1",
          "occupancyLevel": 2,
          "status": "AVAILABLE"
        }
      ]
    }
  ]
}
```

---

### 3.2. Cadastrar Ponto de Coleta
- **Método:** `POST`
- **Endpoint:** `/api/v1/collection-points/`
- **Acesso:** Gestor ou Administrador (`role in ['MANAGER', 'ADMIN']`)
- **Headers:**
  ```http
  Authorization: Bearer <access_token>
  Content-Type: application/json
  ```
- **Campos do Payload (JSON):**
  - `name` *(string, obrigatório)*: Nome identificador do ponto de coleta (ex: `"Campus Central"`).
  - `address` *(string, obrigatório)*: Endereço completo (ex: `"Av. Universitária, 1000"`).
  - `latitude` *(decimal/float, obrigatório)*: Coordenada de latitude (ex: `-16.328123`).
  - `longitude` *(decimal/float, obrigatório)*: Coordenada de longitude (ex: `-48.953456`).
  - `managerId` *(int, opcional)*: ID de um usuário gestor/admin responsável. Se omitido (ou se a requisição for feita por um usuário `MANAGER`), o responsável será automaticamente o próprio criador autenticado. Usuários `ADMIN` podem vincular outro gestor.
  - `trashBins` *(array, opcional)*: Lista de lixeiras a serem criadas vinculadas a este ponto. Aceita tanto uma lista de strings com os códigos (ex: `["B1", "B2"]`) quanto uma lista de objetos (ex: `[{"code": "B1"}, {"code": "B2"}]`).
- **Exemplo de Payload básico:**
```json
{
  "name": "Campus Universitário",
  "address": "Av. Universitária, 1000",
  "latitude": -16.328123,
  "longitude": -48.953456
}
```
- **Exemplo de Payload completo (com gestor e lixeiras iniciais):**
```json
{
  "name": "EcoPonto Central",
  "address": "Praça Cívica, 10",
  "latitude": -16.320000,
  "longitude": -48.940000,
  "managerId": 2,
  "trashBins": ["B1", "B2"]
}
```
- **Resposta (`201 Created`):**
```json
{
  "id": 2,
  "name": "EcoPonto Central",
  "address": "Praça Cívica, 10",
  "latitude": "-16.320000",
  "longitude": "-48.940000",
  "trashBins": [
    {
      "id": 2,
      "code": "B1",
      "occupancyLevel": 1,
      "status": "AVAILABLE"
    },
    {
      "id": 3,
      "code": "B2",
      "occupancyLevel": 1,
      "status": "AVAILABLE"
    }
  ]
}
```

---

### 3.3. Detalhes de um Ponto de Coleta
- **Método:** `GET`
- **Endpoint:** `/api/v1/collection-points/{id}/`
- **Acesso:** Público
- **Parâmetros de Path:**
  - `id` *(int)*: ID do ponto de coleta.
- **Parâmetros de pesquisa (Query Params):** Nenhum
- **Resposta (`200 OK`):**
```json
{
  "id": 1,
  "name": "Campus Principal",
  "address": "Av. Universitária, 100",
  "latitude": "-16.328000",
  "longitude": "-48.953000",
  "trashBins": [
    {
      "id": 1,
      "code": "A1",
      "occupancyLevel": 2,
      "status": "AVAILABLE"
    }
  ]
}
```

---

### 3.4. Listar Lixeiras de um Ponto de Coleta
- **Método:** `GET`
- **Endpoint:** `/api/v1/collection-points/{point_id}/trash-bins/`
- **Acesso:** Público
- **Parâmetros de Path:**
  - `point_id` *(int)*: ID do ponto de coleta.
- **Parâmetros de pesquisa (Query Params):**
  - `page` *(opcional, int)*: Número da página (paginação padrão de 20 itens por página). Exemplo: `?page=1`
- **Resposta (`200 OK`):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "code": "A1",
      "occupancyLevel": 2,
      "status": "AVAILABLE",
      "collectionPointId": 1
    },
    {
      "id": 2,
      "code": "A2",
      "occupancyLevel": 1,
      "status": "AVAILABLE",
      "collectionPointId": 1
    }
  ]
}
```

---

### 3.5. Cadastrar Lixeira em um Ponto de Coleta
- **Método:** `POST`
- **Endpoint:** `/api/v1/collection-points/{point_id}/trash-bins/`
- **Acesso:** Gestor do ponto ou Administrador (`role in ['MANAGER', 'ADMIN']`)
- **Headers:**
  ```http
  Authorization: Bearer <access_token>
  Content-Type: application/json
  ```
- **Parâmetros de Path:**
  - `point_id` *(int)*: ID do ponto de coleta ao qual a lixeira será associada.
- **Campos do Payload (JSON):**
  - `code` *(string, obrigatório)*: Código identificador único da lixeira (ex: `"B1"`).
  - `occupancyLevel` *(int, opcional, default: `1`)*: Nível inicial de ocupação (entre `1` e `4`).
  - `status` *(string, opcional, default: `"AVAILABLE"`)*: Status da lixeira (`"AVAILABLE"`, `"COLLECTION_REQUIRED"`, `"MAINTENANCE"`).
- **Exemplo de Payload:**
```json
{
  "code": "B1",
  "occupancyLevel": 1,
  "status": "AVAILABLE"
}
```
- **Resposta (`201 Created`):**
```json
{
  "id": 3,
  "code": "B1",
  "occupancyLevel": 1,
  "status": "AVAILABLE",
  "collectionPointId": 1
}
```

---

### 3.6. Listar Todas as Lixeiras / Cadastrar com Ponto no Body
- **Endpoint:** `/api/v1/collection-points/trash-bins/`

#### 3.6.1. Listar Lixeiras (GET)
- **Método:** `GET`
- **Acesso:** Autenticado
- **Parâmetros de pesquisa (Query Params):**
  - `collection_point` *(opcional, int)*: Filtrar por ID do ponto de coleta (ex: `?collection_point=1`).
  - `status` *(opcional, string)*: Filtrar por status (`AVAILABLE`, `COLLECTION_REQUIRED`, `MAINTENANCE`).
  - `page` *(opcional, int)*: Paginação (padrão de 20 registros por página). Exemplo: `?page=1`
- **Resposta (`200 OK`):** Lista paginada com todas as lixeiras ativas.

#### 3.6.2. Cadastrar Lixeira (POST)
- **Método:** `POST`
- **Acesso:** Gestor responsável ou Administrador (`role in ['MANAGER', 'ADMIN']`)
- **Headers:**
  ```http
  Authorization: Bearer <access_token>
  Content-Type: application/json
  ```
- **Campos do Payload (JSON):**
  - `collectionPointId` *(int, obrigatório)*: ID do ponto de coleta ativo.
  - `code` *(string, obrigatório)*: Código único da lixeira.
  - `occupancyLevel` *(int, opcional, default: `1`)*: Nível de ocupação (entre `1` e `4`).
  - `status` *(string, opcional, default: `"AVAILABLE"`)*: Status da lixeira.
- **Exemplo de Payload:**
```json
{
  "collectionPointId": 1,
  "code": "C1",
  "occupancyLevel": 1,
  "status": "AVAILABLE"
}
```
- **Resposta (`201 Created`):** Objeto da lixeira criada com status HTTP 201.

---

### 3.7. Consultar Detalhes de uma Lixeira por ID
- **Método:** `GET`
- **Endpoint:** `/api/v1/collection-points/trash-bins/{id}/`
- **Acesso:** Autenticado
- **Parâmetros de Path:**
  - `id` *(int)*: ID da lixeira.
- **Parâmetros de pesquisa (Query Params):** Nenhum
- **Resposta (`200 OK`):**
```json
{
  "id": 1,
  "code": "A1",
  "occupancyLevel": 2,
  "status": "AVAILABLE",
  "collectionPointId": 1
}
```

---

### 3.8. Atualizar Lixeira por ID
- **Método:** `PATCH` (ou `PUT`)
- **Endpoint:** `/api/v1/collection-points/trash-bins/{id}/`
- **Acesso:** Gestor do ponto ou Administrador (`role in ['MANAGER', 'ADMIN']`)
- **Headers:**
  ```http
  Authorization: Bearer <access_token>
  Content-Type: application/json
  ```
- **Parâmetros de Path:**
  - `id` *(int)*: ID da lixeira a ser atualizada.
- **Campos do Payload (todos opcionais em PATCH):**
  - `code` *(string, opcional)*: Novo código da lixeira (deve ser único).
  - `occupancyLevel` *(int, opcional)*: Novo nível de ocupação (entre `1` e `4`).
  - `status` *(string, opcional)*: Novo status (`"AVAILABLE"`, `"COLLECTION_REQUIRED"`, `"MAINTENANCE"`).
  - `collectionPointId` *(int, opcional)*: Novo ID de ponto de coleta caso a lixeira seja movida.
- **Exemplo de Payload (`PATCH`):**
```json
{
  "code": "A1-NOVO",
  "occupancyLevel": 3,
  "status": "MAINTENANCE"
}
```
- **Resposta (`200 OK`):**
```json
{
  "id": 1,
  "code": "A1-NOVO",
  "occupancyLevel": 3,
  "status": "MAINTENANCE",
  "collectionPointId": 1
}
```

> **Atenção (Sem exclusão):** A operação `DELETE` **não é permitida** para lixeiras (`HTTP 405 Method Not Allowed`), garantindo integridade referencial com os históricos de descartes e rastreabilidade das coletas.

---

### 3.9. Consultar Lixeira por Código / QR Code
- **Método:** `GET`
- **Endpoint:** `/api/v1/collection-points/trash-bins/by-code/{code}/`
- **Acesso:** Autenticado
- **Parâmetros de Path:**
  - `code` *(string)*: Código identificador único da lixeira (ex: `A1`).
- **Parâmetros de pesquisa (Query Params):** Nenhum
- **Resposta (`200 OK`):**
```json
{
  "id": 1,
  "code": "A1",
  "occupancyLevel": 2,
  "status": "AVAILABLE",
  "collectionPointId": 1
}
```
> Possíveis valores para `status`: `"AVAILABLE"` (Disponível), `"COLLECTION_REQUIRED"` (Coleta necessária), `"MAINTENANCE"` (Manutenção).

---

## 4. Descartes e Categorias (`/disposals` e `/ranking`)

### 4.1. Listar Categorias de Resíduos
- **Método:** `GET`
- **Endpoint:** `/api/v1/disposals/categories/`
- **Acesso:** Público
- **Parâmetros de pesquisa (Query Params):** Nenhum (retorna a lista completa sem paginação)
- **Resposta (`200 OK`):**
```json
[
  { "id": 5, "name": "Carregadores" },
  { "id": 1, "name": "Computadores" },
  { "id": 4, "name": "Fones" },
  { "id": 6, "name": "Outros" },
  { "id": 2, "name": "Smartphones" },
  { "id": 3, "name": "Tablets" }
]
```

---

### 4.2. Listar Histórico de Descartes do Usuário
- **Método:** `GET`
- **Endpoint:** `/api/v1/disposals/`
- **Acesso:** Autenticado (retorna apenas os descartes do usuário autenticado)
- **Parâmetros de pesquisa (Query Params):**
  - `page` *(opcional, int)*: Número da página (paginação padrão de 20 itens por página). Exemplo: `?page=1`
- **Resposta (`200 OK`):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "date": "03/09/2026",
      "type": "Computadores",
      "quantity": 2,
      "items": "Notebook e teclado",
      "trashLevel": 3,
      "trashCode": "A1",
      "image": "http://localhost:8000/media/disposals/2026/09/proof.jpg",
      "points_awarded": 20
    }
  ]
}
```

---

### 4.3. Registrar Novo Descarte
- **Método:** `POST`
- **Endpoint:** `/api/v1/disposals/`
- **Acesso:** Autenticado
- **Headers:** `Content-Type: multipart/form-data`
- **Campos do Formulário (Payload Multipart):**
  - `trashCode` *(string, obrigatório)*: Código da lixeira ativa (ex: `"A1"`).
  - `categories` *(string, int ou array de int, obrigatório)*: ID(s) da(s) categoria(s) do descarte (ex: `"1"` ou `1`). No envio multipart, aceita string única (`"1"`), lista (`["1"]` ou `[1]`), múltiplos campos (`categories=1`, `categories=2`) ou valores separados por vírgula (`"1,2"`), sendo convertidos automaticamente para inteiros.
  - `quantity` *(string ou int, obrigatório)*: Quantidade de itens descartados (mínimo: `1`). Aceita texto numérico (ex: `"2"`) e converte automaticamente para inteiro.
  - `items` *(string, obrigatório)*: Descrição textual detalhada dos itens.
  - `trashLevel` *(string ou int, obrigatório)*: Nível de ocupação observado na lixeira (valor entre `1` e `4`). Aceita texto numérico (ex: `"3"`) e converte automaticamente para inteiro.
  - `photos` *(arquivo binário de imagem, obrigatório)*: Arquivo de foto comprovatória (ex: `.png`, `.jpg`, `.jpeg`). Suporta tanto arquivo individual quanto lista de fotos.
- **Exemplo de Envio (`multipart/form-data`):**
```text
trashCode: A1
categories: 1
quantity: 2
items: Notebook antigo e teclado
trashLevel: 3
photos: [arquivo de imagem binário]
```
> **Nota:** Como requisições `multipart/form-data` transmitem campos de texto como strings, a API realiza a coerção e higienização automática de strings numéricas para inteiros (`quantity`, `trashLevel` e `categories`), permitindo o envio direto a partir de clientes como Postman e navegadores (`FormData`).

- **Resposta (`201 Created`):**
```json
{
  "id": 1,
  "date": "03/09/2026",
  "type": "Computadores",
  "quantity": 2,
  "items": "Notebook antigo e teclado",
  "trashLevel": 3,
  "trashCode": "A1",
  "image": "http://localhost:8000/media/disposals/2026/09/proof.jpg",
  "points_awarded": 20
}
```

---

### 4.4. Consultar Detalhes de um Descarte Próprio
- **Método:** `GET`
- **Endpoint:** `/api/v1/disposals/{id}/`
- **Acesso:** Proprietário (apenas o criador do descarte pode acessá-lo)
- **Parâmetros de Path:**
  - `id` *(int)*: ID do descarte.
- **Parâmetros de pesquisa (Query Params):** Nenhum
- **Resposta (`200 OK`):**
```json
{
  "id": 1,
  "date": "03/09/2026",
  "type": "Computadores",
  "quantity": 2,
  "items": "Notebook antigo e teclado",
  "trashLevel": 3,
  "trashCode": "A1",
  "image": "http://localhost:8000/media/disposals/2026/09/proof.jpg",
  "points_awarded": 20
}
```

---

### 4.5. Consultar Ranking Geral
- **Método:** `GET`
- **Endpoint:** `/api/v1/ranking/`
- **Acesso:** Público
- **Parâmetros de pesquisa (Query Params):** Nenhum (retorna o top 100 usuários ordenados por pontuação)
- **Resposta (`200 OK`):**
```json
[
  {
    "id": 3,
    "name": "Maria Souza",
    "points": 450,
    "position": 1,
    "avatar": "MS"
  },
  {
    "id": 1,
    "name": "João Silva",
    "points": 120,
    "position": 2,
    "avatar": "JS"
  }
]
```

---

## 5. Notificações (`/notifications`)

### 5.1. Listar Notificações do Gestor
- **Método:** `GET`
- **Endpoint:** `/api/v1/notifications/`
- **Acesso:** Gestor ou Administrador (`role in ['MANAGER', 'ADMIN']`)
- **Parâmetros de pesquisa (Query Params):**
  - `page` *(opcional, int)*: Número da página (paginação padrão de 20 itens por página). Exemplo: `?page=1`
- **Resposta (`200 OK`):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "notification_type": "COLLECTION_REQUIRED",
      "message": "A lixeira A1 atingiu o nível 4 e precisa de coleta.",
      "trashCode": "A1",
      "createdAt": "2026-09-03T21:50:00Z",
      "readAt": null
    }
  ]
}
```

---

### 5.2. Marcar Notificação como Lida
- **Método:** `PATCH`
- **Endpoint:** `/api/v1/notifications/{id}/read/`
- **Acesso:** Destinatário (Gestor/Admin destinatário da notificação)
- **Parâmetros de Path:**
  - `id` *(int)*: ID da notificação a ser marcada como lida.
- **Payload esperado:** Nenhum (corpo da requisição vazio)
- **Resposta (`204 No Content`):** Corpo vazio.

---

## 6. Dashboard e Estatísticas (`/dashboard`)

### 6.1. Consultar Estatísticas de Descartes
- **Método:** `GET`
- **Endpoint:** `/api/v1/dashboard/statistics/`
- **Acesso:** Autenticado
- **Parâmetros de pesquisa (Query Params):**
  - `period` *(opcional, string)*: Janela temporal para filtro dos dados. Se omitido, o padrão é `"6months"`.
    - `"month"`: Últimos 30 dias
    - `"3months"`: Últimos 90 dias
    - `"6months"`: Últimos 180 dias *(default)*
    - `"year"`: Últimos 365 dias
    - Exemplo: `/api/v1/dashboard/statistics/?period=3months`
- **Resposta (`200 OK`):**
```json
{
  "disposals": [
    {
      "month": "Jul",
      "count": 8
    },
    {
      "month": "Aug",
      "count": 15
    },
    {
      "month": "Sep",
      "count": 21
    }
  ],
  "categories": [
    {
      "name": "Computadores",
      "value": 50.0
    },
    {
      "name": "Smartphones",
      "value": 30.0
    },
    {
      "name": "Outros",
      "value": 20.0
    }
  ],
  "totals": {
    "disposals": 44,
    "averageQuantity": 2.2
  }
}
```
