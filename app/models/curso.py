from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

class Curso(SQLModel, table=True):
    nome: str = Field(min_length=3, max_length=100, nullable=False)
    objetivos: str = Field(min_length=3, max_length=500)
    conteudo: str = Field(min_length=3, max_length=1000)
    carga_horaria: int = Field(ge=1, le=200)

