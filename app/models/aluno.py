from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

class Aluno(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    #nome, matricula, cpf, email, data de nascimento, endereco, curso

