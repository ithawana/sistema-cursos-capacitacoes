
from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .turma import Turma
    from .resultado import ResultadoAvaliacao


class AvaliacaoBase(SQLModel):
    titulo: str = Field(max_length=150, nullable=False)
    data: date = Field(default_factory=date.today, nullable=False)
    nota_maxima: float = Field(default=10.0, gt=0, le=10, nullable=False)
    peso: float = Field(default=1.0, gt=0, nullable=False)


class Avaliacao(AvaliacaoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Chave estrangeira
    turma_id: int = Field(foreign_key="turma.id", nullable=False)

    # Relacionamento com turma e resultados das matriculas
    turma: "Turma" = Relationship(back_populates="avaliacoes")
    resultados: list["ResultadoAvaliacao"] = Relationship(back_populates="avaliacao")


class AvaliacaoCreate(AvaliacaoBase):
    turma_id: int


class AvaliacaoUpdate(SQLModel):
    titulo: str | None = None
    data: date | None = None
    nota_maxima: float | None = Field(default=None, gt=0, le=10)
    peso: float | None = Field(default=None, gt=0)
