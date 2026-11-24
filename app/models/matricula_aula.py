
from datetime import date, datetime
from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .matricula import Matricula
    from .aula import Aula


class FrequenciaStatus(str, Enum):
    PRESENTE = "PRESENTE"
    AUSENTE = "AUSENTE"


class Matricula_Aula(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    matricula_id: int = Field(
        foreign_key="matricula.id",
        nullable=False
    )

    aula_id: int = Field(
        foreign_key="aula.id",
        nullable=False
    )

    frequencia: FrequenciaStatus = Field(
        default=FrequenciaStatus.PRESENTE
    )

    data_aula: date = Field(
        default_factory=date.today,
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "matricula_id",
            "aula_id",
            name="uq_matricula_aula"
        ),
    )

    matricula: "Matricula" = Relationship(back_populates="frequencias")
    aula: "Aula" = Relationship(back_populates="frequencias")


class MatriculaAulaCreate(SQLModel):
    matricula_id: int
    aula_id: int
    frequencia: FrequenciaStatus = FrequenciaStatus.PRESENTE


class MatriculaAulaPublic(SQLModel):
    id: int
    matricula_id: int
    aula_id: int
    frequencia: FrequenciaStatus
    data_aula: date


class MatriculaAulaUpdate(SQLModel):
    frequencia: FrequenciaStatus | None = None
