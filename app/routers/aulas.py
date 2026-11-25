
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from sqlmodel import Session

from app.database import getSession
from app.models.aula import AulaCreate, AulaPublic, AulaUpdate
from app.crud import aula as crud


router = APIRouter(
    prefix="/aulas",
    tags=["Aulas"]
)


#Cadastrar aula
@router.post("/", response_model=AulaPublic, status_code=201)
def criar_aula(
    dados: AulaCreate,
    session: Session = Depends(getSession),
):
    try:
        return crud.criar_aula(dados, session)

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Erro ao cadastrar a aula"
        )


#Listar aulas
@router.get("/", response_model=list[AulaPublic])
def listar_aulas(
    turma_id: int | None = None,
    session: Session = Depends(getSession),
):
    return crud.listar_aulas(session, turma_id)


#Buscar aula por ID
@router.get("/{aula_id}", response_model=AulaPublic)
def buscar_aula(
    aula_id: int,
    session: Session = Depends(getSession),
):
    aula = crud.buscar_aula(aula_id, session)

    if not aula:
        raise HTTPException(
            status_code=404,
            detail="Aula não encontrada"
        )

    return aula


#Atualizar aula
@router.patch("/{aula_id}", response_model=AulaPublic)
def atualizar_aula(
    aula_id: int,
    dados: AulaUpdate,
    session: Session = Depends(getSession),
):
    try:
        aula = crud.atualizar_aula(
            aula_id, dados, session
        )

        if not aula:
            raise HTTPException(
                status_code=404,
                detail="Aula não encontrada"
            )

        return aula

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
            detail="Erro na atualização da aula"
        )


#Excluir aula
@router.delete("/{aula_id}", status_code=204)
def excluir_aula(
    aula_id: int,
    session: Session = Depends(getSession),
):
    try:
        excluida = crud.excluir_aula(aula_id, session)

        if not excluida:
            raise HTTPException(
                status_code=404,
                detail="Aula não encontrada"
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
            detail="Aula não pode ser removida"
        )
