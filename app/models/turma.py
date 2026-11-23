from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

class TurmaBase(SQLModel, table=True):
    numero_vagas: int = Field(default=30, nullable=False)
    data_inicio: date = Field(default=datetime.now().date(), nullable=False)
    data_fim: date = Field(default=datetime.now().date(), nullable=False)


class Turma(TurmaBase, table=True):
    id: int = Field(default=None, primary_key=True)
    # relacionar curso, instrutor, aula, matricula, avaliacao


class TurmaCreate(TurmaBase):
    pass


class TurmaUpdate(TurmaBase):
    numero_vagas: int | None = None
    data_inicio: date | None = None
    data_fim: date | None = None
