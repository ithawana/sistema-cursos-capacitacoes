from fastapi import FastAPI
from app.routers import alunos
from app.routers import matriculas
from app.routers import aulas
from app.routers import avaliacoes
from app.routers import consultas

app = FastAPI()

app.include_router(alunos.router)
app.include_router(matriculas.router)
app.include_router(aulas.router)
app.include_router(avaliacoes.router)
app.include_router(consultas.router)


@app.get("/")
def inicio():
    return {"Hello, World!"}