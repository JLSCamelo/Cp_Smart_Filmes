from pydantic import BaseModal, Field


#####-----Generos----#######
class GeneroBase(BaseModel):
    nome: str

class GeneroCreate(GeneroBase):
    pass

class GeneroResponse(GeneroBase):
    id: int
    class Config:
        from_attribuites=True

#####-----Filmes----#######

class FilmeBase(BaseModel):
    titulo: str
    classificacao: str = Field(..., examples=["Livre", "12 anos", "16 anos", "18 anos"])
    nota: float = Field(..., ge=0, le=10)
    genero_id: int

class FIlmeCreate(FilmeBase):
    pass

class FilmeResponse(FilmeBase):
    id: int
    genero: GeneroResponse

    class Config:
        from_attributes=True