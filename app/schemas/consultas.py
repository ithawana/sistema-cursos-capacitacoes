from datetime import date
from sqlmodel import SQLModel

from app.models.matricula import MatriculaStatus


# Situação dos participantes de uma turma
class ParticipanteTurma(SQLModel):
    matricula_id: int
    aluno_id: int
    aluno_nome: str
    aluno_email: str
    status: MatriculaStatus
    data_matricula: date
    data_cancelamento: date | None


# Histórico de capacitações de um aluno
class HistoricoCapacitacao(SQLModel):
    matricula_id: int
    curso_id: int
    curso_nome: str
    carga_horaria: int
    turma_id: int
    turma_data_inicio: date
    turma_data_fim: date
    instrutor_nome: str
    status: MatriculaStatus
    data_matricula: date


# Matrículas filtradas por situação
class MatriculaSituacao(SQLModel):
    matricula_id: int
    status: MatriculaStatus
    data_matricula: date
    data_cancelamento: date | None
    aluno_id: int
    aluno_nome: str
    turma_id: int
    curso_id: int
    curso_nome: str


# Ranking de cursos por quantidade de concluintes
class CursoConcluintes(SQLModel):
    curso_id: int
    curso_nome: str
    total_concluintes: int


# Frequência de cada aluno
class FrequenciaAluno(SQLModel):
    matricula_id: int
    aluno_id: int
    aluno_nome: str
    status: MatriculaStatus
    aulas_realizadas: int
    presencas: int
    percentual_frequencia: float | None
    frequencia_minima: float
    abaixo_do_minimo: bool


# Estatísticas
class EstatisticaCurso(SQLModel):
    curso_id: int
    curso_nome: str
    total_turmas: int
    total_matriculas: int
    matriculas_por_status: dict[str, int]
    taxa_aprovacao: float | None
    media_notas: float | None


class Estatisticas(SQLModel):
    total_alunos: int
    total_cursos: int
    total_turmas: int
    matriculas_por_status: dict[str, int]
    cursos: list[EstatisticaCurso]
