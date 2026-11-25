from fastapi import FastAPI
from app.routers import alunos
from app.routers import matriculas

app = FastAPI()

app.include_router(alunos.router)
app.include_router(matriculas.router)


@app.get("/")
def inicio():
    return {"Hello, World!"}