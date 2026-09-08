from fastapi import FastAPI
from database import Base, engine
from controller import router

#para rodar: uvicorn main:app --reload
Base.Metadata.create_all(bind=engine)

app=FastAPI(
    title="Api de filmes",
    description="API para gerenciar filmes organizados por gênero, classificação e nota",
    version = "1.0.0",
    )
app.incluide_router(router)
@app.get("/")
def root():
    return{"mensagem": "API de Filmes rodando"}