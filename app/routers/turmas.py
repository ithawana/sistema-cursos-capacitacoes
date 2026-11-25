from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.database import getSession
from app.models.turma import TurmaCreate, TurmaPublic, TurmaUpdate
from app.crud import turma as crud

router = APIRouter(prefix="/turmas", tags=["Turmas"])

@router.post("/", response_model=TurmaPublic, status_code=201)
def criar_turma(dados: TurmaCreate, session: Session = Depends(getSession)):
    try:
        return crud.criar_turma(dados, session)
    except HTTPException:
        raise
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Conflito de integridade no cadastro da turma")

@router.get("/", response_model=list[TurmaPublic])
def listar_turmas(session: Session = Depends(getSession)):
    return crud.listar_turmas(session)

@router.get("/{turma_id}", response_model=TurmaPublic)
def buscar_turma(turma_id: int, session: Session = Depends(getSession)):
    turma = crud.buscar_turma(turma_id, session)
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return turma

@router.patch("/{turma_id}", response_model=TurmaPublic)
def atualizar_turma(turma_id: int, dados: TurmaUpdate, session: Session = Depends(getSession)):
    try:
        turma = crud.atualizar_turma(turma_id, dados, session)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        return turma
    except HTTPException:
        raise
    except ValidationError:
        raise HTTPException(status_code=422, detail="Dados inválidos para atualização da turma")
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Conflito de integridade na atualização da turma")

@router.delete("/{turma_id}", status_code=204)
def excluir_turma(turma_id: int, session: Session = Depends(getSession)):
    try:
        excluida = crud.excluir_turma(turma_id, session)
        if not excluida:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
    except ValueError as erro:
        raise HTTPException(status_code=409, detail=str(erro))
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Turma possui vínculos e não pode ser removida")