from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

class AlunoBase(SQLModel, table=True):
    nome: str = Field(max_length=150, nullable=False)
    cpf: str = Field(max_length=11, nullable=False, unique=True)
    email: str = Field(max_length=100, nullable=False, unique=True)
    data_nascimento: date = Field(nullable=False)

class Aluno(AlunoBase, table=True):
    id: int = Field(default=None, primary_key=True)
    # relacionar com endereco e matricula
    
class AlunoCreate(AlunoBase):
    pass

class AlunoPublic(AlunoBase):
    id: int

class AlunoUpdate(SQLModel):
    nome: str | None = None
    cpf: str | None = None
    email: str | None = None
    data_nascimento: date | None = None

