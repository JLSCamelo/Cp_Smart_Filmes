from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from schemas import FilmeCreate, FilmeResponse, GeneroCreate, GeneroResponse
import service

router = APIRouter()

# --- Rotas de Gênero --- #

@router.post("/generos", response_model=GeneroResponse)
def criar_genero(genero: GeneroCreate, db: Session = Depends(get_db)):
    novo_genero = service.criar_genero(db, genero)
    if not novo_genero:
        raise HTTPException(status_code=400, detail="Genero já existe")
    return novo_genero


@router.get("/generos", response_model=List[GeneroResponse])
def listar_generos(db: Session = Depends(get_db)):
    return service.listar_generos(db)


@router.get("/generos/{genero_id}", response_model=GeneroResponse)
def obter_genero(genero_id: int, db: Session = Depends(get_db)):
    genero = service.buscar_genero(db, genero_id)
    if not genero:
        raise HTTPException(status_code=404, detail="Genero não encontrado")
    return genero


# ---- Rotas de Filme ----- #
#
# NOTA PARA QUEM MEXER NA PARTE 3 (Controller):
# O campo "poster_path" (ex: "acao/batman.webp") já vem incluso no
# FilmeCreate e no FilmeResponse (ver schemas.py), então as rotas abaixo
# já aceitam e devolvem ele sem precisar de nenhuma mudança.
#
# O que muda pra vocês:
# - Ao TESTAR no Swagger (/docs), o poster_path é só um texto, precisa
#   bater com o nome real do arquivo dentro da pasta filmes/<genero>/.
# - A pasta filmes/ já está configurada como estática no main.py
#   (app.mount("/imagens", ...)), então a imagem de um filme fica
#   acessível em: http://127.0.0.1:8000/imagens/{poster_path}
#   Ex: poster_path = "acao/batman.webp" -> /imagens/acao/batman.webp
# - Se quiserem uma rota tipo GET /filmes/{id}/poster que já devolve a
#   URL completa (em vez do frontend montar ela), é só criar aqui.

@router.post("/filmes", response_model=FilmeResponse)
def criar_filme(filme: FilmeCreate, db: Session = Depends(get_db)):
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
):
    return service.listar_filmes(db, genero_id, classificacao, nota_minima)


@router.get("/filmes/{filme_id}", response_model=FilmeResponse)
def obter_filme(filme_id: int, db: Session = Depends(get_db)):
    filme = service.buscar_filme(db, filme_id)
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return filme


@router.delete("/filmes/{filme_id}")
def deletar_filme(filme_id: int, db: Session = Depends(get_db)):
    sucesso = service.excluir_filme(db, filme_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return {"detail": "Filme removido com sucesso"}
