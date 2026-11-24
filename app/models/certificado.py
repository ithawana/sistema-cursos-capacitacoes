
from datetime import date, datetime
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .matricula import Matricula


class CertificadoBase(SQLModel):
    data_emissao: date = Field(default_factory=date.today, nullable=False)
    codigo_validacao: str = Field(max_length=50, unique=True, nullable=False)


class Certificado(CertificadoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Chave estrangeira
    matricula_id: int = Field(
        foreign_key="matricula.id",
        unique=True,
        nullable=False
    )

    # Relacionamento com Matricula
    matricula: "Matricula" = Relationship(back_populates="certificado")


class CertificadoCreate(SQLModel):
    matricula_id: int


class CertificadoPublic(CertificadoBase):
    id: int
    matricula_id: int


class CertificadoUpdate(SQLModel):
    data_emissao: date | None = None
    codigo_validacao: str | None = None