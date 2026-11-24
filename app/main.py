from fastapi import FastAPI
from app.routers import alunos

app = FastAPI()

app.include_router(alunos.router)


@app.get("/")
def inicio():
    return {"Hello, World!"}