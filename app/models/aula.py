
from datetime import date, datetime, time
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .turma import Turma
    from .matricula_aula import Matricula_Aula


class AulaBase(SQLModel):
    data: date = Field(default_factory=date.today, nullable=False)
    horario: time = Field(default_factory=lambda: datetime.now().time(), nullable=False)
    duracao: int = Field(default=60, ge=1, nullable=False)  # em minutos
    conteudo: str = Field(default="", nullable=False)


class Aula(AulaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Chave estrangeira
    turma_id: int = Field(foreign_key="turma.id", nullable=False)

    # Relacionamentos com turma e matricula
    turma: "Turma" = Relationship(back_populates="aulas")
    frequencias: list["Matricula_Aula"] = Relationship(back_populates="aula")


class AulaCreate(AulaBase):
    turma_id: int


class AulaUpdate(AulaBase):
    data: date | None = None
    horario: time | None = None
    duracao: int | None = None
    conteudo: str | None = None