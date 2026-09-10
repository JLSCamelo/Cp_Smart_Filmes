# Smart FIlmes

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-07405E?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/license-academic-lightgrey)

#ALUNOS RESPONSÁVEIS:
Arthur: RM:568878
Henrique: RM:570740
Julia: RM: 574139
Vinicius: RM:564379

API REST para gerenciamento de um catálogo de filmes, organizados por gênero, classificação indicativa e nota, com autenticação de usuário via JWT.

Desenvolvido com **FastAPI**, **SQLAlchemy** e **SQLite** no backend, e um frontend em **HTML, CSS e JavaScript** que consome essa API.

---

## Sumário

- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Instalação e execução](#instalação-e-execução)
- [Endpoints da API](#endpoints-da-api)
- [Autenticação](#autenticação)
- [Licença](#licença)

---

## Funcionalidades

- Cadastro e login de usuário, com senha protegida por hash e autenticação via token JWT
- CRUD completo de filmes e gêneros
- Filtros de busca por gênero, classificação indicativa e nota mínima
- Armazenamento e distribuição dos pôsteres dos filmes como arquivos estáticos
- Script de seed para popular o banco com um catálogo inicial de filmes
- Documentação interativa gerada automaticamente (Swagger UI)

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | FastAPI |
| Banco de dados | SQLite + SQLAlchemy |
| Validação | Pydantic |
| Autenticação | JWT (python-jose) + bcrypt |
| Servidor | Uvicorn |
| Frontend | HTML, CSS, JavaScript |

## Estrutura do projeto

```
main.py           Ponto de entrada da aplicação
controller.py      Definição das rotas da API
service.py          Regras de negócio
models.py            Modelos de dados (SQLAlchemy)
schemas.py            Schemas de validação (Pydantic)
database.py            Configuração da conexão com o banco
security.py              Hash de senha e geração/validação de JWT
seed_filmes.py             Script de população inicial do banco
requirements.txt            Dependências do projeto
filmes/                       Pôsteres dos filmes
frontend/                       Interface web
```

## Instalação e execução

**Pré-requisito:** Python 3.9 ou superior.

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Inicie a aplicação:

   ```bash
   uvicorn main:app --reload
   ```

   A API estará disponível em `http://127.0.0.1:8000`, com documentação interativa em `http://127.0.0.1:8000/docs`.

3. (Opcional) Popule o banco com um catálogo inicial de filmes:

   ```bash
   python seed_filmes.py
   ```

4. Para utilizar a interface web, abra `frontend/index.html` no navegador ou sirva a pasta com:

   ```bash
   cd frontend
   python3 -m http.server 5500
   ```

   Nesse caso, acesse `http://127.0.0.1:5500`.

## Endpoints da API

| Método | Rota | Autenticação | Descrição |
|---|---|:---:|---|
| POST | `/auth/registrar` | — | Cria uma conta de usuário |
| POST | `/auth/login` | — | Autentica e retorna o token de acesso |
| GET | `/auth/me` | Sim | Retorna os dados do usuário autenticado |
| GET / POST | `/generos` | Sim | Lista ou cria gêneros |
| GET / PUT / DELETE | `/generos/{id}` | — | Consulta, atualiza ou remove um gênero |
| GET / POST | `/filmes` | Sim | Lista (com filtros) ou cadastra filmes |
| GET / PUT / DELETE | `/filmes/{id}` | — | Consulta, atualiza ou remove um filme |

A listagem de filmes aceita os parâmetros de consulta `genero_id`, `classificacao` e `nota_minima`.

## Autenticação

O acesso às rotas protegidas requer um token JWT, obtido em `/auth/login` e enviado no cabeçalho das requisições:

```
Authorization: Bearer <token>
```

As senhas são armazenadas com hash via bcrypt; em nenhum momento a senha original é persistida ou retornada pela API.

## Licença

Projeto desenvolvido para fins acadêmicos.
