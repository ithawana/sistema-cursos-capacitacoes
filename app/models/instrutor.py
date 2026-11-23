from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

class InstrutorBase(SQLModel, table=True):
    nome: str = Field(max_length=150, nullable=False)
    cpf: str = Field(max_length=11, nullable=False, unique=True)
    email: str = Field(max_length=100, nullable=False, unique=True)
    data_nascimento: date = Field(nullable=False)


class Instrutor(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    # relacionar com turma


class InstrutorCreate(InstrutorBase):
    pass


class InstrutorUpdate(SQLModel):
    nome: str | None = None
    cpf: str | None = None
    email: str | None = None
    data_nascimento: date | None = None