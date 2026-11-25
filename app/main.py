from fastapi import FastAPI
from app.routers import alunos
from app.routers import matriculas
from app.routers import cursos
from app.routers import instrutores

app = FastAPI()

app.include_router(alunos.router)
app.include_router(matriculas.router)
app.include_router(cursos.router)
app.include_router(instrutores.router)


@app.get("/")
def inicio():
    return {"Hello, World!"}