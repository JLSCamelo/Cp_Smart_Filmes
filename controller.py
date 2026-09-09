from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from schemas import (
    FilmeCreate,
    FilmeResponse,
    GeneroCreate,
    GeneroResponse,
    UsuarioCreate,
    UsuarioResponse,
    UsuarioLogin,
    Token,
)
from security import criar_access_token, obter_usuario_atual
from models import Usuario
import service

router = APIRouter()

# --- Rotas de Autenticação --- #

@router.post("/auth/registrar", response_model=UsuarioResponse)
def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    novo_usuario = service.criar_usuario(db, usuario)
    if not novo_usuario:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    return novo_usuario


@router.post("/auth/login", response_model=Token)
def login(dados: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = service.autenticar_usuario(db, dados.email, dados.senha)
    if not usuario:
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")
    token = criar_access_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/auth/me", response_model=UsuarioResponse)
def me(usuario_atual: Usuario = Depends(obter_usuario_atual)):
    return usuario_atual

# --- Rotas de Gênero --- #

@router.post("/generos", response_model=GeneroResponse)
def criar_genero(
    genero: GeneroCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    novo_genero = service.criar_genero(db, genero)
    if not novo_genero:
        raise HTTPException(status_code=400, detail="Genero já existe")
    return novo_genero


@router.get("/generos", response_model=List[GeneroResponse])
def listar_generos(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    return service.listar_generos(db)


@router.get("/generos/{genero_id}", response_model=GeneroResponse)
def obter_genero(genero_id: int, db: Session = Depends(get_db)):
    genero = service.buscar_genero(db, genero_id)
    if not genero:
        raise HTTPException(status_code=404, detail="Genero não encontrado")
    return genero


@router.put("/generos/{genero_id}", response_model=GeneroResponse)
def atualizar_genero(genero_id: int, genero: GeneroCreate, db: Session = Depends(get_db)):
    atualizado = service.atualizar_genero(db, genero_id, genero)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Genero não encontrado")
    return atualizado


@router.delete("/generos/{genero_id}")
def deletar_genero(genero_id: int, db: Session = Depends(get_db)):
    resultado = service.excluir_genero(db, genero_id)
    if resultado == "nao_encontrado":
        raise HTTPException(status_code=404, detail="Genero não encontrado")
    if resultado == "possui_filmes":
        raise HTTPException(
            status_code=400,
            detail="Não é possível excluir: existem filmes cadastrados nesse gênero"
        )
    return {"detail": "Genero removido com sucesso"}

@router.post("/filmes", response_model=FilmeResponse)
def criar_filme(
    filme: FilmeCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    novo_filme = service.criar_filme(db, filme)
    if not novo_filme:
        raise HTTPException(status_code=404, detail="Genero informado não existe")
    return novo_filme


@router.get("/filmes", response_model=List[FilmeResponse])
def listar_filmes(
    genero_id: Optional[int] = None,
    classificacao: Optional[str] = None,
    nota_minima: Optional[float] = None,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    return service.listar_filmes(db, genero_id, classificacao, nota_minima)


@router.get("/filmes/{filme_id}", response_model=FilmeResponse)
def obter_filme(filme_id: int, db: Session = Depends(get_db)):
    filme = service.buscar_filme(db, filme_id)
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return filme

@router.put("/filmes/{filme_id}", response_model=FilmeResponse)
def atualizar_filme(filme_id: int, filme: FilmeCreate, db: Session = Depends(get_db)):
    resultado = service.atualizar_filme(db, filme_id, filme)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    if resultado == "genero_invalido":
        raise HTTPException(status_code=404, detail="Genero informado não existe")
    return resultado


@router.delete("/filmes/{filme_id}")
def deletar_filme(filme_id: int, db: Session = Depends(get_db)):
    sucesso = service.excluir_filme(db, filme_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return {"detail": "Filme removido com sucesso"}
