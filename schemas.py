from typing import Optional
from pydantic import BaseModel, Field  # Corrigido: BaseModel

#####-----Gêneros----#######
class GeneroBase(BaseModel):
    nome: str

class GeneroCreate(GeneroBase):
    pass

class GeneroResponse(GeneroBase):
    id: int

    class Config:
        from_attributes = True  

#####-----Filmes----#######

class FilmeBase(BaseModel):
    titulo: str
    classificacao: str = Field(..., examples=["Livre", "12 anos", "16 anos", "18 anos"])
    nota: float = Field(..., ge=0, le=10)
    genero_id: int
    poster_path: Optional[str] = None

class FilmeCreate(FilmeBase):  
    pass

class FilmeResponse(FilmeBase):
    id: int
    genero: GeneroResponse

    class Config:
        from_attributes = True