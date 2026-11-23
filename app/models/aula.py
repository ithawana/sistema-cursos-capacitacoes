from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

class AulaBase(SQLModel, table=True):
    data: date = Field(default=date.today, nullable=False)
    horario: datetime = Field(default=datetime.now, nullable=False)
    duracao: int = Field(default=60, nullable=False)  # em minutos
    conteudo: str = Field(default="", nullable=False)

class Aula(AulaBase, table=True):
    id: int = Field(default=None, primary_key=True)
    # relacionar com turma e matricula (frequencia)

class AulaCreate(AulaBase):
    pass    

class AulaUpdate(AulaBase):
    data: date | None = None
    horario: datetime | None = None
    duracao: int | None = None
    conteudo: str | None = None