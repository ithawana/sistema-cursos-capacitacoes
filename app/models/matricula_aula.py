from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum

class FrequenciaStatus(str, Enum):
    PRESENTE = "PRESENTE"
    AUSENTE = "AUSENTE"

class Matricula_Aula(SQLModel, table=True):
    matricula_id: int | None = Field(
        default=None,
        foreign_key="matricula.id",
        primary_key=True,
    )
    aula_id: int | None = Field(
        default=None,
        foreign_key="aula.id",
        primary_key=True,
    )

    id: int = Field(default=None, primary_key=True)
    frequencia: FrequenciaStatus = Field(default=FrequenciaStatus.PRESENTE)
    data_aula: date = Field(
        default=datetime.now().date(), 
        nullable=False, 
        table=True
    )
    
    
