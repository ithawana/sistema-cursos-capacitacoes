
from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .turma import Turma

class InstrutorBase(SQLModel):
    nome: str = Field(max_length=150, nullable=False)
    cpf: str = Field(max_length=11, nullable=False, unique=True)
    email: str = Field(max_length=100, nullable=False, unique=True)
    data_nascimento: date = Field(nullable=False)


class Instrutor(InstrutorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    turmas: list["Turma"] = Relationship(back_populates="instrutor")


class InstrutorCreate(InstrutorBase):
    pass


class InstrutorPublic(InstrutorBase):
    id: int
    

class InstrutorUpdate(SQLModel):
    nome: str | None = None
    cpf: str | None = None
    email: str | None = None
    data_nascimento: date | None = None
