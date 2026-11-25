from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from sqlmodel import Session

from app.database import getSession
from app.models.matricula import (
    MatriculaCreate,
    MatriculaPublic,
    MatriculaUpdate
)
from app.crud import matricula as crud


router = APIRouter(
    prefix="/matriculas",
    tags=["Matriculas"]
)


#Cadastrar matricula
@router.post("/", response_model=MatriculaPublic, status_code=201)
def criar_matricula(
    dados: MatriculaCreate,
    session: Session = Depends(getSession),
):
    try:
        return crud.criar_matricula(dados, session)

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Conflito de integridade no cadastro da matrícula"
        )


#Listar matriculas
@router.get("/", response_model=list[MatriculaPublic])
def listar_matriculas(
    session: Session = Depends(getSession),
):
    return crud.listar_matriculas(session)


#Buscar matricula por ID
@router.get("/{matricula_id}", response_model=MatriculaPublic)
def buscar_matricula(
    matricula_id: int,
    session: Session = Depends(getSession),
):
    matricula = crud.buscar_matricula(matricula_id, session)

    if not matricula:
        raise HTTPException(
            status_code=404,
            detail="Matrícula não encontrada"
        )

    return matricula


#Atualizar matricula
@router.patch("/{matricula_id}", response_model=MatriculaPublic)
def atualizar_matricula(
    matricula_id: int,
    dados: MatriculaUpdate,
    session: Session = Depends(getSession),
):
    try:
        matricula = crud.atualizar_matricula(
            matricula_id, dados, session
        )

        if not matricula:
            raise HTTPException(
                status_code=404,
                detail="Matrícula não encontrada"
            )

        return matricula

    except ValidationError:
        raise HTTPException(
            status_code=422,
            detail="Dados inválidos para atualização da matrícula"
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
            detail="Erro na atualização da matrícula"
        )


#Cancelar matricula
@router.delete("/{matricula_id}", status_code=204)
def cancelar_matricula(
    matricula_id: int,
    session: Session = Depends(getSession),
):
    try:
        cancelada = crud.cancelar_matricula(
            matricula_id, session
        )

        if not cancelada:
            raise HTTPException(
                status_code=404,
                detail="Matrícula não encontrada"
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
            detail="Não é possível cancelar a matrícula"
        )