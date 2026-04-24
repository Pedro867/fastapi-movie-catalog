# Catálogo de Filmes (Movie Catalog API)

Uma API desenvolvida em FastAPI para gerenciar um catálogo de filmes. O projeto permite realizar operações de CRUD (Criar, Ler e Deletar) de filmes em um banco de dados relacional.

## 🚀 Funcionalidades

- Listar todos os filmes
- Buscar um filme específico pelo ID
- Adicionar um novo filme ao catálogo
- Remover um filme do catálogo

## 🛠️ Stack e Bibliotecas Principais

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

1. **Clone o repositório e acesse a pasta**

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

Aqui estão as rotas disponíveis na aplicação:

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/movies/` | Retorna a lista de todos os filmes. Suporta paginação (`skip`, `limit`). |
| `POST` | `/movies/` | Adiciona um novo filme. |
| `GET` | `/movies/{movie_id}`| Retorna os detalhes de um filme específico. |
| `DELETE`| `/movies/{movie_id}`| Remove um filme pelo seu ID. |

## 📁 Estrutura do Projeto

```text
Filmes/
├── app/
│   ├── main.py        # Ponto de entrada da aplicação e rotas
│   ├── database.py    # Configuração de conexão com o banco de dados
│   ├── models.py      # Modelos do SQLAlchemy (Tabelas do banco)
│   ├── schemas.py     # Modelos do Pydantic (Validação de entrada/saída)
│   └── crud.py        # Funções para interagir com o banco de dados
├── tests/             # Diretório de testes
├── .env               # Variáveis de ambiente (não versionado)
├── requirements.txt   # Dependências do projeto
└── README.md          # Documentação do projeto
```