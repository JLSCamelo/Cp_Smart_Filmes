from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from controller import router

#para rodar: uvicorn main:app --reload
Base.metadata.create_all(bind=engine)

app=FastAPI(
    title="Api de filmes",
    description="API para gerenciar filmes organizados por gênero, classificação e nota",
    version = "1.0.0",
    )
app.include_router(router)

# Serve a pasta filmes/ (imagens dos pôsteres) via URL, ex: /imagens/acao/batman.webp
app.mount("/imagens", StaticFiles(directory="filmes"), name="imagens")

@app.get("/")
def root():
    return{"mensagem": "API de Filmes rodando"}