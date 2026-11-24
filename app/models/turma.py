
from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .curso import Curso
    from .instrutor import Instrutor
    from .aula import Aula
    from .matricula import Matricula
    from .avaliacao import Avaliacao


class TurmaBase(SQLModel):
    numero_vagas: int = Field(default=30, ge=1, nullable=False)
    data_inicio: date = Field(default_factory=date.today, nullable=False)
    data_fim: date = Field(default_factory=date.today, nullable=False)
    frequencia_minima: float = Field(default=75.0, ge=0, le=100, nullable=False)
    nota_minima: float | None = Field(default=7.0, ge=0, le=10)


class Turma(TurmaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Chave estrangeira
    curso_id: int = Field(foreign_key="curso.id", nullable=False)
    instrutor_id: int = Field(foreign_key="instrutor.id", nullable=False)

    # relacionar curso, instrutor, aula, matricula, avaliacao
    curso: "Curso" = Relationship(back_populates="turmas")
    instrutor: "Instrutor" = Relationship(back_populates="turmas")
    aulas: list["Aula"] = Relationship(back_populates="turma")
    matriculas: list["Matricula"] = Relationship(back_populates="turma")
    avaliacoes: list["Avaliacao"] = Relationship(back_populates="turma")


class TurmaCreate(TurmaBase):
    curso_id: int
    instrutor_id: int


class TurmaUpdate(TurmaBase):
    numero_vagas: int | None = Field(default=None, ge=1)
    data_inicio: date | None = None
    data_fim: date | None = None
    frequencia_minima: float | None = Field(default=None, ge=0, le=100)
    nota_minima: float | None = Field(default=None, ge=0, le=10)
    curso_id: int | None = None
    instrutor_id: int | None = None
