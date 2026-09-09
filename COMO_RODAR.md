# Cine Henrique — Como rodar

Este projeto tem duas partes:

- **Backend** (`main.py` e arquivos ao redor): API em FastAPI, que guarda os dados no banco `filmes.db` (SQLite). Agora com login/cadastro de usuário de verdade (senha com hash, token JWT).
- **Frontend** (pasta `frontend/`): site em HTML puro + CSS + JavaScript, que consome essa API.

## 1. Rodar o backend

No terminal, dentro da pasta do projeto:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

A API vai subir em `http://127.0.0.1:8000`.
Você pode conferir a documentação automática em `http://127.0.0.1:8000/docs`.

> Se você mudar a porta ou o host, atualize a constante `API_BASE` no arquivo `frontend/app.js`.

### Cadastrar automaticamente os filmes que já têm pôster salvo

O projeto já vem com pôsteres nas pastas `filmes/acao`, `filmes/animacao`, `filmes/comedia`,
`filmes/romance` e `filmes/terror`, mas nenhum filme cadastrado no banco. Pra popular o banco
com esses 51 filmes de uma vez (título, gênero, classificação e nota já preenchidos a partir
do pôster), rode:

```bash
python seed_filmes.py
```

Pode rodar quantas vezes quiser: ele pula os filmes que já existem, então não duplica nada.
Título/classificação/nota são um "melhor esforço" — edite pela API (`/docs`) se quiser ajustar
algum depois.


## 2. Abrir o site

Dentro da pasta `frontend/`, basta abrir o arquivo `index.html` no navegador
(duplo clique, ou clique direito → abrir com o navegador).

Se o navegador bloquear as requisições por causa de `file://`, rode um
servidor simples só para os arquivos estáticos (numa aba de terminal separada):

```bash
cd frontend
python3 -m http.server 5500
```

E acesse `http://127.0.0.1:5500` no navegador.

## 3. Fluxo de uso

1. Abra o site → como você ainda não está logado, ele te leva para **Criar conta**.
2. Crie sua conta (nome, e-mail, senha).
3. Faça **login**.
4. Você cai no catálogo, que lista os filmes já salvos no banco (filtrando por gênero,
   classificação e nota mínima).
5. Clique em **"+ Cadastrar filme"** para adicionar um filme novo. Se o gênero que você
   quer ainda não existir, dá pra criar um gênero novo na mesma tela.

## O que foi adicionado no backend original

O repositório original (`Cp_Smart_Filmes`) só tinha rotas de `Genero` e `Filme`, sem nenhum
sistema de usuário. Para o site pedir login de verdade, foram adicionados:

- `models.py`: tabela `Usuario` (nome, e-mail, senha em hash)
- `security.py`: geração de hash de senha (bcrypt) e criação/validação de token JWT
- `schemas.py`: schemas de `UsuarioCreate`, `UsuarioResponse`, `UsuarioLogin`, `Token`
- `service.py`: funções `criar_usuario` e `autenticar_usuario`
- `controller.py`: rotas `POST /auth/registrar`, `POST /auth/login`, `GET /auth/me`, e as
  rotas de gêneros/filmes agora exigem estar logado (token no cabeçalho `Authorization`)
- `main.py`: liberação de CORS, para o site em HTML poder chamar a API

Nenhum filme de exemplo foi pré-cadastrado no banco automaticamente pelo backend — mas agora
existe o script `seed_filmes.py`, que cadastra os 51 filmes cujos pôsteres já estão nas pastas
`filmes/acao`, `filmes/comedia`, etc. Basta rodar `python seed_filmes.py` depois de instalar as
dependências (veja a seção acima).
