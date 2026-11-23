from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum

class MatriculaStatus(str, Enum):
    ATIVA = "ATIVA"
    INATIVA = "INATIVA"
    CANCELADA = "CANCELADA"


class MatriculaBase(SQLModel, table=True):
    status: MatriculaStatus = Field(default=MatriculaStatus.ATIVA, nullable=False)
    data_matricula: date = Field(default=datetime.now().date(), nullable=False)
    data_cancelamento: date | None = Field(default=None, nullable=True)
    
class Matricula(MatriculaBase, table=True):
    id: int = Field(default=None, primary_key=True)
    # relacionar com avaliacao, aluno, turma(n-n), aula(n-n)
    
class MatriculaCreate(MatriculaBase):
    pass

class MatriculaUpdate(MatriculaBase):
    status: MatriculaStatus | None = None
    data_matricula: date | None = None
    data_cancelamento: date | None = None