
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.database import getSession
from app.models.matricula import MatriculaStatus
from app.schemas.consultas import (
    ParticipanteTurma,
    HistoricoCapacitacao,
    MatriculaSituacao,
    CursoConcluintes,
    FrequenciaAluno,
    Estatisticas,
)
from app.crud import consultas as crud


router = APIRouter(
    prefix="/consultas",
    tags=["Consultas"]
)


# Situação dos participantes de uma turma
@router.get("/turmas/{turma_id}/participantes",response_model=list[ParticipanteTurma])
def participantes_turma(
    turma_id: int,
    status: MatriculaStatus | None = Query(default=None, description="Filtrar por situação"),
    session: Session = Depends(getSession),
):
    return crud.participantes_turma(session, turma_id, status)


# Histórico de capacitações de um aluno
@router.get("/alunos/{aluno_id}/historico", response_model=list[HistoricoCapacitacao])
def historico_aluno(
    aluno_id: int,
    session: Session = Depends(getSession),
):
    return crud.historico_aluno(session, aluno_id)


# Matrículas por situação 
@router.get("/matriculas/situacao", response_model=list[MatriculaSituacao])
def matriculas_por_situacao(
    status: MatriculaStatus = Query(description="Situação procurada"),
    curso_id: int | None = Query(default=None),
    turma_id: int | None = Query(default=None),
    session: Session = Depends(getSession),
):
    return crud.matriculas_por_situacao(session, status, curso_id, turma_id)


# Cursos com maior quantidade de concluintes
@router.get("/cursos/mais-concluintes", response_model=list[CursoConcluintes])
def cursos_mais_concluintes(
    limite: int = Query(default=5, ge=1, le=50),
    session: Session = Depends(getSession),
):
    return crud.cursos_mais_concluintes(session, limite)


# Frequência dos alunos
@router.get("/turmas/{turma_id}/frequencia", response_model=list[FrequenciaAluno])
def frequencia_turma(
    turma_id: int,
    apenas_abaixo_minimo: bool = Query(default=False),
    session: Session = Depends(getSession),
):
    return crud.frequencia_turma(session, turma_id, apenas_abaixo_minimo)


# Estatísticas 
@router.get("/estatisticas", response_model=Estatisticas)
def estatisticas(
    session: Session = Depends(getSession),
):
    return crud.estatisticas(session)
