
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from sqlmodel import Session

from app.database import getSession
from app.models.avaliacao import (
    AvaliacaoCreate,
    AvaliacaoPublic,
    AvaliacaoUpdate
)
from app.crud import avaliacao as crud


router = APIRouter(
    prefix="/avaliacoes",
    tags=["Avaliacoes"]
)


# Cadastrar avaliação
@router.post("/", response_model=AvaliacaoPublic, status_code=201)
def criar_avaliacao(
    dados: AvaliacaoCreate,
    session: Session = Depends(getSession),
):
    try:
        return crud.criar_avaliacao(dados, session)

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Ocorreu um erro no cadastro da avaliação"
        )


# Listar avaliações
@router.get("/", response_model=list[AvaliacaoPublic])
def listar_avaliacoes(
    turma_id: int | None = None,
    session: Session = Depends(getSession),
):
    return crud.listar_avaliacoes(session, turma_id)


# Buscar por ID
@router.get("/{avaliacao_id}", response_model=AvaliacaoPublic)
def buscar_avaliacao(
    avaliacao_id: int,
    session: Session = Depends(getSession),
):
    avaliacao = crud.buscar_avaliacao(avaliacao_id, session)

    if not avaliacao:
        raise HTTPException(
            status_code=404,
            detail="Avaliação não encontrada"
        )

    return avaliacao


# Atualizar avaliação
@router.patch("/{avaliacao_id}", response_model=AvaliacaoPublic)
def atualizar_avaliacao(
    avaliacao_id: int,
    dados: AvaliacaoUpdate,
    session: Session = Depends(getSession),
):
    try:
        avaliacao = crud.atualizar_avaliacao(
            avaliacao_id, dados, session
        )

        if not avaliacao:
            raise HTTPException(
                status_code=404,
                detail="Avaliação não encontrada"
            )

        return avaliacao

    except ValidationError:
        raise HTTPException(
            status_code=422,
            detail="Dados inválidos"
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Erro na atualização da avaliação"
        )


# Excluir avaliação
@router.delete("/{avaliacao_id}", status_code=204)
def excluir_avaliacao(
    avaliacao_id: int,
    session: Session = Depends(getSession),
):
    try:
        excluida = crud.excluir_avaliacao(avaliacao_id, session)

        if not excluida:
            raise HTTPException(
                status_code=404,
                detail="Avaliação não encontrada"
            )

    except ValueError as erro:
        raise HTTPException(
            status_code=409,
            detail=str(erro)
        )

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Avaliação não pode ser removida"
        )
