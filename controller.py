from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Filme, Genero
from schemas import FilmeCreate, FilmeResponse, GeneroCreate, GeneroResponse

router = APIRouter()

# --- Rotas de Gênero --- #

@router.post("/generos", response_model=GeneroResponse)
def criar_genero(genero: GeneroCreate, db: Session = Depends(get_db)):
    existente = db.query(Genero).filter(Genero.nome == genero.nome).first()
    if existente:
        raise HTTPException(status_code=400, detail="Genero já existe")

    novo_genero = Genero(**genero.model_dump())
    db.add(novo_genero)
    db.commit()
    db.refresh(novo_genero)
    return novo_genero

@router.get("/generos", response_model=List[GeneroResponse])
def listar_generos(db: Session = Depends(get_db)): 
    return db.query(Genero).all()

@router.get("/generos/{genero_id}", response_model=GeneroResponse) 
def obter_genero(genero_id: int, db: Session = Depends(get_db)):
    genero = db.query(Genero).filter(Genero.id == genero_id).first()
    if not genero:
        raise HTTPException(status_code=404, detail="Genero não encontrado")
    return genero

# ---- Rotas de Filme ----- #

@router.post("/filmes", response_model=FilmeResponse)
def criar_filme(filme: FilmeCreate, db: Session = Depends(get_db)):
    genero = db.query(Genero).filter(Genero.id == filme.genero_id).first()
    if not genero: 
        raise HTTPException(status_code=404, detail="Genero informado não existe")
        
    novo_filme = Filme(**filme.model_dump())
    db.add(novo_filme)
    db.commit()
    db.refresh(novo_filme)
    return novo_filme

@router.get("/filmes", response_model=List[FilmeResponse])
def listar_filmes(
    genero_id: Optional[int] = None,
    classificacao: Optional[str] = None,
    nota_minima: Optional[float] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Filme)

    if genero_id is not None:
        query = query.filter(Filme.genero_id == genero_id)
    if classificacao is not None:
        query = query.filter(Filme.classificacao == classificacao)
    if nota_minima is not None:
        query = query.filter(Filme.nota >= nota_minima)

    return query.all()

@router.get("/filmes/{filme_id}", response_model=FilmeResponse)  
def obter_filme(filme_id: int, db: Session = Depends(get_db)):
    filme = db.query(Filme).filter(Filme.id == filme_id).first()
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return filme

@router.delete("/filmes/{filme_id}")  
def deletar_filme(filme_id: int, db: Session = Depends(get_db)):
    filme = db.query(Filme).filter(Filme.id == filme_id).first()
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

    db.delete(filme)
    db.commit()
    return {"detail": "Filme removido com sucesso"}