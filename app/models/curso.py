
from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .turma import Turma

class CursoBase(SQLModel):
    nome: str = Field(max_length=100, nullable=False, unique=True)
    objetivos: str = Field(min_length=3, max_length=500)
    conteudo_programatico: str = Field(min_length=3, max_length=500)
    carga_horaria: int = Field(ge=1, le=200)

class Curso(CursoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    turmas: list["Turma"] = Relationship(back_populates="curso")

class CursoCreate(CursoBase):
    pass

class CursoPublic(CursoBase):
    id: int

class CursoUpdate(SQLModel):
    nome: str | None = None
    objetivos: str | None = None
    conteudo_programatico: str | None = None
    carga_horaria: int | None = Field(default=None, ge=1, le=200)
