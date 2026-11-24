
from datetime import date, datetime
from typing import Optional
from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .aluno import Aluno
    from .turma import Turma
    from .matricula_aula import Matricula_Aula
    from .resultado import ResultadoAvaliacao
    from .certificado import Certificado


class MatriculaStatus(str, Enum):
    ATIVA = "ATIVA"
    INATIVA = "INATIVA"
    CANCELADA = "CANCELADA"
    ABANDONADA = "ABANDONADA"
    APROVADA = "APROVADA"
    REPROVADA = "REPROVADA"


class MatriculaBase(SQLModel):
    status: MatriculaStatus = Field(default=MatriculaStatus.ATIVA, nullable=False)
    data_matricula: date = Field(default_factory=date.today, nullable=False)
    data_cancelamento: date | None = Field(default=None, nullable=True)


class Matricula(MatriculaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Chave estrangeira
    aluno_id: int = Field(foreign_key="aluno.id", nullable=False)
    turma_id: int = Field(foreign_key="turma.id", nullable=False)

    # não deixa o aluno ter duas matriculas na mesma turma
    __table_args__ = (
        UniqueConstraint("aluno_id", "turma_id", name="uq_matricula_aluno_turma"),
    )

    aluno: "Aluno" = Relationship(back_populates="matriculas")
    turma: "Turma" = Relationship(back_populates="matriculas")

    frequencias: list["Matricula_Aula"] = Relationship(back_populates="matricula")
    resultados_avaliacao: list["ResultadoAvaliacao"] = Relationship(back_populates="matricula")
    certificado: Optional["Certificado"] = Relationship(back_populates="matricula")


class MatriculaCreate(MatriculaBase):
    aluno_id: int
    turma_id: int


class MatriculaPublic(MatriculaBase):
    id: int
    aluno_id: int
    turma_id: int



class MatriculaUpdate(SQLModel):
    status: MatriculaStatus | None = None
    data_matricula: date | None = None
    data_cancelamento: date | None = None