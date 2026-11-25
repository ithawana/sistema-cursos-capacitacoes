from fastapi import FastAPI
from app.routers import alunos
from app.routers import matriculas
from app.routers import aulas
from app.routers import avaliacoes
from app.routers import consultas
from app.routers import cursos
from app.routers import instrutores
from app.routers import turmas
from app.routers import frequencias
from app.routers import resultados

app = FastAPI()

app.include_router(alunos.router)
app.include_router(matriculas.router)
app.include_router(aulas.router)
app.include_router(avaliacoes.router)
app.include_router(cursos.router)
app.include_router(instrutores.router)
app.include_router(turmas.router)
app.include_router(consultas.router)
app.include_router(frequencias.router)
app.include_router(resultados.router)
