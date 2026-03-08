# Flix API

API REST para cadastro e consulta de filmes, gêneros, atores e avaliações, construída com Django REST Framework e autenticação JWT.

## Tecnologias

- Python 3.12+
- Django 5.2.8
- Django REST Framework 3.16.1
- Simple JWT 5.5.1
- SQLite (padrão do projeto)

## Pré-requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)
- git (para clonar o repositório)

## Estrutura do Projeto

- `authentication`: autenticação JWT
- `actors`: cadastro de atores
- `genres`: cadastro de gêneros
- `movies`: cadastro de filmes e estatísticas
- `reviews`: avaliações de filmes

## Como Executar Localmente

1. Clone o repositório e entre na pasta do projeto:
   ```bash
   git clone <url-do-repositorio>
   cd flix_api
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Rode as migrações:
   ```bash
   python manage.py migrate
   ```

5. (Opcional) Crie um superusuário para acessar o admin:
   ```bash
   python manage.py createsuperuser
   ```

6. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

A API ficará disponível em:

- `http://127.0.0.1:8000/api/v1/`
- Admin Django: `http://127.0.0.1:8000/admin/`

## Autenticação

A API usa JWT em todas as rotas de recursos.

### Obter token

`POST /api/v1/authentication/token/`

Exemplo de corpo:

```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

Exemplo com curl:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/authentication/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"seu_usuario","password":"sua_senha"}'
```

Resposta esperada:

```json
{
  "refresh": "...",
  "access": "..."
}
```

### Renovar token

`POST /api/v1/authentication/token/refresh/`

Corpo da requisição:

```json
{
  "refresh": "..."
}
```

### Verificar token

`POST /api/v1/authentication/token/verify/`

Corpo da requisição:

```json
{
  "token": "..."
}
```

### Header de autorização

Em todas as requisições autenticadas, inclua o header:

```http
Authorization: Bearer <access_token>
```

Exemplo com curl:

```bash
curl -X GET http://127.0.0.1:8000/api/v1/movies/ \
  -H "Authorization: Bearer <access_token>"
```

## Permissões

- Todas as rotas exigem usuário autenticado.
- `actors`, `genres` e `movies` também usam permissão por modelo do Django (`view`, `add`, `change`, `delete`).
- `reviews` exige apenas autenticação.

Se necessário, use o admin (`/admin/`) para atribuir permissões ao usuário ou grupo.

## Endpoints

Prefixo base: `/api/v1`

### Actors

- `GET /actors/` - Listar todos os atores
- `POST /actors/` - Criar novo ator
- `GET /actors/{id}/` - Obter detalhes de um ator
- `PUT /actors/{id}/` - Atualizar ator completamente
- `PATCH /actors/{id}/` - Atualizar parcialmente um ator
- `DELETE /actors/{id}/` - Deletar ator

Campos:

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `name` | string | Sim | Nome do ator |
| `birthday` | date | Não | Data de nascimento |
| `nationality` | string | Não | Nacionalidade (`USA` ou `BRAZIL`) |

Exemplo de criação:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/actors/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Tom Hanks","birthday":"1956-07-09","nationality":"USA"}'
```

### Genres

- `GET /genres/` - Listar todos os gêneros
- `POST /genres/` - Criar novo gênero
- `GET /genres/{id}/` - Obter detalhes de um gênero
- `PUT /genres/{id}/` - Atualizar gênero completamente
- `PATCH /genres/{id}/` - Atualizar parcialmente um gênero
- `DELETE /genres/{id}/` - Deletar gênero

Campos:

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `name` | string | Sim | Nome do gênero |

Exemplo de criação:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/genres/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Action"}'
```

### Movies

- `GET /movies/` - Listar todos os filmes
- `POST /movies/` - Criar novo filme
- `GET /movies/{id}/` - Obter detalhes de um filme
- `PUT /movies/{id}/` - Atualizar filme completamente
- `PATCH /movies/{id}/` - Atualizar parcialmente um filme
- `DELETE /movies/{id}/` - Deletar filme
- `GET /movies/stats/` - Obter estatísticas dos filmes

Campos de escrita (`POST/PUT/PATCH`):

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `title` | string | Sim | Título do filme |
| `genre` | integer | Sim | ID do gênero |
| `actors` | array | Sim | Lista de IDs de atores |
| `release_date` | date | Não | Data de lançamento (>= 1990) |
| `resume` | string | Não | Sinopse (máx. 200 caracteres) |

Campos de leitura (`GET`):

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | integer | ID do filme |
| `title` | string | Título do filme |
| `genre` | object | Gênero aninhado |
| `actors` | array | Atores aninhados |
| `release_date` | date | Data de lançamento |
| `resume` | string | Sinopse |
| `rate` | float | Média das estrelas das avaliações |

Exemplo de criação:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/movies/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Forrest Gump","genre":1,"actors":[1,2],"release_date":"1994-07-06","resume":"A história de um homem com bom coração."}'
```

### Reviews

- `GET /reviews/` - Listar todas as avaliações
- `POST /reviews/` - Criar nova avaliação
- `GET /reviews/{id}/` - Obter detalhes de uma avaliação
- `PUT /reviews/{id}/` - Atualizar avaliação completamente
- `PATCH /reviews/{id}/` - Atualizar parcialmente uma avaliação
- `DELETE /reviews/{id}/` - Deletar avaliação

Campos:

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `movie` | integer | Sim | ID do filme |
| `stars` | integer | Sim | Avaliação (0 a 5) |
| `comment` | string | Não | Comentário opcional |

Exemplo de criação:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/reviews/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"movie":1,"stars":5,"comment":"Filme excelente!"}'
```

## Comando de Importação de Atores

O projeto inclui um comando de management para importar atores via CSV:

```bash
python manage.py import_actors actors_100.csv
```

O CSV deve ter as colunas:

- `name`
- `birthday` (formato `YYYY-MM-DD`)
- `nationality` (`USA` ou `BRAZIL`)

## Qualidade de Código

Para análise estática com flake8:

```bash
# Instale as dependências de desenvolvimento
pip install -r requeriments_dev.txt

# Execute o flake8
flake8 .
```

Configuração atual (`.flake8`):
- Ignora arquivos em `.venv`
- Ignora erro E501 (linha muito longa)

## Exemplos de Uso

### Fluxo completo de utilização da API

```bash
# 1. Obter token de acesso
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/v1/authentication/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r '.access')

# 2. Criar um gênero
curl -X POST http://127.0.0.1:8000/api/v1/genres/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Drama"}'

# 3. Listar gêneros (para obter o ID)
curl -X GET http://127.0.0.1:8000/api/v1/genres/ \
  -H "Authorization: Bearer $TOKEN"

# 4. Criar um filme
curl -X POST http://127.0.0.1:8000/api/v1/movies/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"O Poderoso Chefão","genre":1,"actors":[1,2]}'

# 5. Criar uma avaliação
curl -X POST http://127.0.0.1:8000/api/v1/reviews/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"movie":1,"stars":5,"comment":"Obra-prima!"}'

# 6. Listar filmes com avaliações
curl -X GET http://127.0.0.1:8000/api/v1/movies/ \
  -H "Authorization: Bearer $TOKEN"
```

## Troubleshooting

### Erro de permissão (403 Forbidden)

Certifique-se de que o usuário tem as permissões necessárias no Django Admin:
1. Acesse `/admin/`
2. Vá em `Authentication and Authorization` > `Users`
3. Selecione o usuário e adicione as permissões dos apps (`actors`, `genres`, `movies`, `reviews`)

### Erro de token expirado

Obtenha um novo token ou use o endpoint de refresh:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/authentication/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<refresh_token>"}'
```

## Observações

- O projeto está com `DEBUG=True` e `ALLOWED_HOSTS=['*']`, adequado apenas para desenvolvimento.
- Para produção, ajuste configurações de segurança, banco de dados e variáveis sensíveis.
- O tempo de vida do token de acesso é de 1 dia e do refresh token é de 7 dias (configurável em `app/settings.py`).

## Licença

Este projeto está sob a licença MIT.
