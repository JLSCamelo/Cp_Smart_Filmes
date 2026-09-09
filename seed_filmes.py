"""
Script de seed: cadastra no banco os filmes cujos pôsteres já existem
na pasta filmes/, usando o nome do arquivo pra identificar o filme.

Rode uma vez, depois de criar o banco (ou a qualquer momento -- ele pula
filmes que já foram cadastrados antes, então é seguro rodar de novo):

    python seed_filmes.py

Título, classificação indicativa e nota são um "melhor esforço" a partir
do pôster/arquivo -- edite pelo site ou pela API se quiser ajustar algo.
"""

from database import Base, engine, SessionLocal
from models import Genero, Filme

Base.metadata.create_all(bind=engine)

# genero -> lista de (arquivo, titulo, classificacao, nota)
FILMES = {
    "Ação": [
        ("acao/batman.webp", "Batman", "12 anos", 7.8),
        ("acao/deadpool.webp", "Deadpool", "18 anos", 8.0),
        ("acao/duna.webp", "Duna", "12 anos", 8.0),
        ("acao/gladiador.webp", "Gladiador", "16 anos", 8.5),
        ("acao/homemaranha.webp", "Homem-Aranha", "12 anos", 7.4),
        ("acao/matrix.webp", "Matrix", "16 anos", 8.7),
        ("acao/senhordosaneis.webp", "O Senhor dos Anéis: A Sociedade do Anel", "12 anos", 8.8),
        ("acao/superman.webp", "Superman", "Livre", 7.3),
        ("acao/velozesefuriosos.webp", "Velozes e Furiosos", "14 anos", 6.8),
        ("acao/vingadores.webp", "Vingadores", "12 anos", 8.0),
    ],
    "Animação": [
        ("animacao/abelaeafera.webp", "A Bela e a Fera", "Livre", 7.1),
        ("animacao/aranhaverso.webp", "Homem-Aranha no Aranhaverso", "10 anos", 8.4),
        ("animacao/divertidamente.webp", "Divertida Mente", "Livre", 8.1),
        ("animacao/enrolados.webp", "Enrolados", "Livre", 7.7),
        ("animacao/minions.webp", "Minions", "Livre", 6.4),
        ("animacao/moana.webp", "Moana: Um Mar de Aventuras", "Livre", 7.6),
        ("animacao/ratatouillr.webp", "Ratatouille", "Livre", 8.1),
        ("animacao/reileao.webp", "O Rei Leão", "Livre", 8.5),
        ("animacao/toystory.webp", "Toy Story", "Livre", 8.3),
        ("animacao/up.webp", "Up: Altas Aventuras", "Livre", 8.3),
    ],
    "Comédia": [
        ("comedia/500diascomasummer.webp", "500 Dias com Ela", "12 anos", 7.7),
        ("comedia/autodacompadecida.webp", "Auto da Compadecida", "12 anos", 8.6),
        ("comedia/badboys.webp", "Bad Boys para Sempre", "16 anos", 6.5),
        ("comedia/diabovesteprada.webp", "O Diabo Veste Prada", "12 anos", 7.4),
        ("comedia/eraumavezemholliwood.webp", "Era Uma Vez em... Hollywood", "16 anos", 7.6),
        ("comedia/lalalend.webp", "La La Land: Cantando Estações", "Livre", 8.0),
        ("comedia/mamamia.webp", "Mamma Mia!", "Livre", 6.6),
        ("comedia/nottinghill.webp", "Um Lugar Chamado Notting Hill", "12 anos", 7.2),
        ("comedia/panico.webp", "Pânico", "16 anos", 6.6),
        ("comedia/superbad.webp", "Superbad: É Hoje", "16 anos", 7.6),
    ],
    "Romance": [
        ("romance/10coisasqeuodeioemvc.webp", "10 Coisas Que Eu Odeio em Você", "12 anos", 7.3),
        ("romance/amoresmaterialistas.webp", "Amores Materialistas", "14 anos", 6.0),
        ("romance/antesdevoce.webp", "Como Eu Era Antes de Você", "14 anos", 7.7),
        ("romance/aspatricinhasdebeverlyhills.webp", "As Patricinhas de Beverly Hills", "Livre", 6.9),
        ("romance/derepente30.webp", "De Repente 30", "12 anos", 6.7),
        ("romance/diariodeumapaixao.webp", "Diário de uma Paixão", "12 anos", 7.8),
        ("romance/mechamepeloseunome.webp", "Me Chame pelo Seu Nome", "16 anos", 7.9),
        ("romance/orgulhoepreconceito.webp", "Orgulho e Preconceito", "Livre", 7.8),
        ("romance/prettywoman.webp", "Uma Linda Mulher", "14 anos", 7.0),
        ("romance/quehoraseutepego.webp", "Sem Filtro", "16 anos", 6.3),
        ("romance/titanic.webp", "Titanic", "12 anos", 7.9),
    ],
    "Terror": [
        ("terror/alien.webp", "Alien, o Oitavo Passageiro", "16 anos", 8.4),
        ("terror/carrie.webp", "Carrie, a Estranha", "16 anos", 7.4),
        ("terror/exoscista.webp", "O Exorcista", "18 anos", 8.0),
        ("terror/halloween.webp", "Halloween", "16 anos", 7.7),
        ("terror/hereditario.webp", "Hereditário", "18 anos", 7.3),
        ("terror/midsommar.webp", "Midsommar: O Mal Não Espera a Noite", "18 anos", 7.1),
        ("terror/obcessao.webp", "Obsessão", "16 anos", 5.8),
        ("terror/sextafeira13.webp", "Sexta-Feira 13", "16 anos", 6.4),
        ("terror/substancia.webp", "A Substância", "18 anos", 7.5),
        ("terror/terrifeir.webp", "Terrifier", "18 anos", 5.3),
    ],
}


def rodar_seed():
    db = SessionLocal()
    try:
        criados_genero = 0
        criados_filme = 0
        pulados = 0

        for nome_genero, filmes in FILMES.items():
            genero = db.query(Genero).filter(Genero.nome == nome_genero).first()
            if not genero:
                genero = Genero(nome=nome_genero)
                db.add(genero)
                db.commit()
                db.refresh(genero)
                criados_genero += 1

            for poster_path, titulo, classificacao, nota in filmes:
                ja_existe = (
                    db.query(Filme)
                    .filter(Filme.titulo == titulo, Filme.genero_id == genero.id)
                    .first()
                )
                if ja_existe:
                    pulados += 1
                    continue

                novo_filme = Filme(
                    titulo=titulo,
                    classificacao=classificacao,
                    nota=nota,
                    poster_path=poster_path,
                    genero_id=genero.id,
                )
                db.add(novo_filme)
                criados_filme += 1

        db.commit()
        print(f"Gêneros criados: {criados_genero}")
        print(f"Filmes cadastrados: {criados_filme}")
        print(f"Filmes já existentes (pulados): {pulados}")
    finally:
        db.close()


if __name__ == "__main__":
    rodar_seed()
