
from datetime import date, datetime
from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .matricula import Matricula
    from .avaliacao import Avaliacao


class ResultadoAvaliacaoBase(SQLModel):
    nota: float = Field(ge=0, le=10, nullable=False)
    comentario: str = Field(default="", max_length=100, nullable=True)


class ResultadoAvaliacao(ResultadoAvaliacaoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Chave estrangeira
    matricula_id: int = Field(foreign_key="matricula.id", nullable=False)
    avaliacao_id: int = Field(foreign_key="avaliacao.id", nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "matricula_id",
            "avaliacao_id",
            name="uq_resultado_avaliacao"
        ),
    )

    matricula: "Matricula" = Relationship(back_populates="resultados_avaliacao")
    avaliacao: "Avaliacao" = Relationship(back_populates="resultados")


class ResultadoAvaliacaoCreate(ResultadoAvaliacaoBase):
    matricula_id: int
    avaliacao_id: int


class ResultadoAvaliacaoPublic(ResultadoAvaliacaoBase):
    id: int
    matricula_id: int
    avaliacao_id: int


class ResultadoAvaliacaoUpdate(SQLModel):
    nota: float | None = Field(default=None, ge=0, le=10)
    comentario: str | None = None