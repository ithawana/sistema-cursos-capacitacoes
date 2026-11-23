from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

class AvaliacaoBase(SQLModel, table=True):
    nota: float = Field(default=0.0, nullable=False)
    comentario: str = Field(default="", max_length=100, nullable=True)

class Avaliacao(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    # relacionar com turma, matricula (??)

class AvaliacaoCreate(AvaliacaoBase):
    pass

class AvaliacaoUpdate(SQLModel):
    nota: float | None = None
    comentario: str | None = None
