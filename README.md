# FastAPI Movie Catalog - RESTful Nível 2

Uma API robusta desenvolvida em FastAPI para gerenciar um catálogo de filmes. Este projeto foi construído com um foco profundo em **arquitetura de software** e boas práticas de **design de APIs RESTful**, servindo como base de aprendizado avançado para a criação de APIs modernas em qualquer linguagem (como Node.js, Go, etc).

## 🚀 Funcionalidades

- **CRUD Completo:** Listar (todos e por ID), Adicionar, Substituir (Total), Atualizar (Parcial) e Remover filmes.
- **Respostas Envelopadas:** Todas as rotas seguem um contrato estrito de resposta JSON usando um Schema Genérico do Pydantic (`StandardResponse`).
- **Paginação:** Suporte integrado a paginação nas listagens.

## 🏛️ Destaques da Arquitetura RESTful

Este projeto foi refatorado para seguir os padrões da indústria e atingir o **Modelo de Maturidade de Richardson (Nível 2)**:
- **Design de Recursos:** URIs construídas exclusivamente com substantivos (`/movies/`).
- **Semântica de Verbos HTTP:**
  - `GET` para leitura sem efeitos colaterais.
  - `POST` para criação de recursos.
  - `PUT` para atualização integral do recurso.
  - `PATCH` para atualização parcial (recebendo chaves dinâmicas).
  - `DELETE` para exclusões.
- **Status Codes Precisos:** Retornos semânticos como `201 Created` para inserções, `200 OK` para sucesso, `404 Not Found` para ausência de recursos e `500 Internal Server Error`.
- **Cabeçalho Location:** Respostas de POST informam ativamente a URI do recurso recém-criado nos *headers* HTTP.
- **Transações Seguras:** Camada de banco de dados (CRUD) isolada e blindada com tratamento de exceções (`try...except` com `db.rollback()`), garantindo a integridade da sessão do SQLAlchemy.

## 🛠️ Stack e Bibliotecas Principais
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Uvicorn](https://img.shields.io/badge/uvicorn-2094F3?style=for-the-badge&logo=python&logoColor=white)
![RESTful](https://img.shields.io/badge/RESTful-Level_2-green?style=for-the-badge)

- **Linguagem:** Python 3.14.0
- **Framework Web:** FastAPI 0.136.0
- **Servidor:** Uvicorn 0.44.0
- **ORM:** SQLAlchemy 2.0.49
- **Banco de Dados:** PostgreSQL (psycopg2 2.9.12)
- **Validação de Dados:** Pydantic 2.13.2
- **Variáveis de Ambiente:** python-dotenv 1.2.2

## ⚙️ Pré-requisitos

Antes de iniciar, certifique-se de ter o seguinte instalado:
- Python 3.9+ (Atualmente usando 3.14)
- PostgreSQL
- Um gerenciador de ambientes virtuais (como `venv`)

Você precisará criar um arquivo `.env` na raiz do projeto contendo a URL de conexão com o banco de dados:

```env
DATABASE_URL="postgresql://usuario:senha@localhost:5432/nome_do_banco"
```

## 📦 Instalação e Execução

Siga os passos abaixo para rodar o projeto localmente:

1. **Clone o repositório e acesse a pasta do projeto.**

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**
   *Lembre-se de rodar a partir do diretório raiz do projeto (onde está a pasta `app`).*
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Acesse a documentação:**
   A API estará disponível em `http://127.0.0.1:8000`.
   O FastAPI gera documentação interativa automaticamente. Você pode acessá-la em:
   - **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🛤️ Endpoints da API

A API expõe o recurso `/movies` aplicando rigidamente a semântica REST:

| Método   | Rota                 | Status HTTP | Descrição |
|----------|----------------------|-------------|-----------|
| `GET`    | `/movies/`           | `200 OK`    | Retorna a lista padronizada de filmes (`data: [...]`). |
| `POST`   | `/movies/`           | `201 Created`| Cria um novo filme e retorna a URI no Header `Location`. |
| `GET`    | `/movies/{movie_id}` | `200 OK`    | Retorna os detalhes encapsulados de um filme. |
| `PUT`    | `/movies/{movie_id}` | `200 OK`    | Substitui completamente os dados de um filme. |
| `PATCH`  | `/movies/{movie_id}` | `200 OK`    | Atualiza parcialmente os dados do filme (JSON flexível). |
| `DELETE` | `/movies/{movie_id}` | `200 OK`    | Remove um filme pelo seu ID. |

## 🧪 Testes

O projeto conta com uma suíte de testes automatizados utilizando `pytest` e `TestClient` do FastAPI, alcançando a marca de **100% de coverage de testes unitários**. Eles utilizam um banco de dados SQLite temporário para garantir que os testes rodem rapidamente e de forma isolada, sem afetar o banco de desenvolvimento.

Para executar os testes, a partir do diretório raiz do projeto, execute o comando:

```bash
pytest
```

Os testes cobrem:
- **Criação** (POST) e validação de schemas Pydantic.
- **Listagem** e leitura de itens específicos (GET).
- **Atualização** (PUT e PATCH).
- **Remoção** (DELETE).
- **Tratamento de Erros**, validando o retorno de Status Codes apropriados (ex: `404 Not Found` ao buscar um ID inexistente).
- **Testes de Integração (End-to-End)**, validando o ciclo de vida completo de um recurso e cenários negativos (dados inválidos, IDs inexistentes).

## 📁 Estrutura do Projeto

```text
fastapi-movie-catalog/
├── app/
│   ├── main.py        # Ponto de entrada, Rotas REST e Definição de Status HTTP
│   ├── database.py    # Configuração de conexão com o banco de dados
│   ├── models.py      # Modelos do SQLAlchemy (Tabelas do PostgreSQL)
│   ├── schemas.py     # Modelos do Pydantic (Generic Types e StandardResponse)
│   └── crud.py        # Isolamento da Regra de Negócio e Transações DB
├── tests/             # Diretório de testes
├── .env               # Variáveis de ambiente (não versionado)
├── requirements.txt   # Dependências do projeto
└── README.md          # Documentação do projeto
```
