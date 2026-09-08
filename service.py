from typing import Optional

from sqlalchemy.orm import Session

from models import Filme, Genero
from schemas import FilmeCreate, GeneroCreate


# ---------- Genero ----------

def criar_genero(db: Session, dados: GeneroCreate):
    """Cria um gênero, retorna None se já existir um com o mesmo nome."""
    existente = db.query(Genero).filter(Genero.nome == dados.nome).first()
    if existente:
        return None

    novo_genero = Genero(**dados.model_dump())
    db.add(novo_genero)
    db.commit()
    db.refresh(novo_genero)
    return novo_genero


def listar_generos(db: Session):
    return db.query(Genero).all()


def buscar_genero(db: Session, genero_id: int):
    return db.query(Genero).filter(Genero.id == genero_id).first()


# ---------- Filme ----------

def criar_filme(db: Session, dados: FilmeCreate):
    """Cria um filme, retorna None se o genero_id informado não existir."""
    genero = buscar_genero(db, dados.genero_id)
    if not genero:
        return None

    novo_filme = Filme(**dados.model_dump())
    db.add(novo_filme)
    db.commit()
    db.refresh(novo_filme)
    return novo_filme


def listar_filmes(
    db: Session,
    genero_id: Optional[int] = None,
    classificacao: Optional[str] = None,
    nota_minima: Optional[float] = None,
):
    """Lista filmes, com filtros opcionais por gênero, classificação e nota mínima."""
    query = db.query(Filme)

    if genero_id is not None:
        query = query.filter(Filme.genero_id == genero_id)
    if classificacao is not None:
        query = query.filter(Filme.classificacao == classificacao)
    if nota_minima is not None:
        query = query.filter(Filme.nota >= nota_minima)

    return query.all()


def buscar_filme(db: Session, filme_id: int):
    return db.query(Filme).filter(Filme.id == filme_id).first()


def excluir_filme(db: Session, filme_id: int):
    """Remove um filme, retorna False se ele não existir."""
    filme = buscar_filme(db, filme_id)
    if not filme:
        return False

    db.delete(filme)
    db.commit()
    return True
