from sqlmodel import SQLModel
from app.models.aluno import AlunoPublic


class MetadadosPaginacao(SQLModel):
    total_registros: int
    total_paginas: int
    pagina_atual: int
    tamanho_pagina: int


class PaginaAlunos(SQLModel):
    dados: list[AlunoPublic]
    paginacao: MetadadosPaginacao