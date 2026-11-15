from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

class Aula(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    #data, horario, duracao, conteudo, turma
