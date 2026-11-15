from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

class Instrutor(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    # nome, cpf, matricula, email, especialidade, historico
