from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

class CursoBase(SQLModel, table=True):
    nome: str = Field(max_length=100, nullable=False, unique=True)
    objetivos: str = Field(min_length=3, max_length=500)
    conteudo_programatico: str = Field(min_length=3, max_length=500)
    carga_horaria: int = Field(ge=1, le=200)

class Curso(CursoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # relacionar com turma

class CursoCreate(CursoBase):
    pass

class CursoPublic(CursoBase):
    id: int

class CursoUpdate(SQLModel):
    nome: str | None = None
    objetivos: str | None = None
    conteudo_programatico: str | None = None
    carga_horaria: int | None = Field(default=None, ge=1, le=200)