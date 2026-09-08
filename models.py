from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Genero(Base):
    __tablename__ = "generos"

    id=Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)

    filmes=relationship("Filme", back_populates="genero")

class Filme(Base):
    __tablename__="filmes"
    id=Column(Integer, primary_key=True, index=True)
    titulo=Column(String,nullable=False)
    nota=Column(Float, nullable=False)

    genero_id=Column(Integer, ForeignKey("generos.id"), nullable=False)
    genero=relationship("Genero", back_populates="filmes")
    