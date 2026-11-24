
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from pydantic import ValidationError

from app.database import getSession
from app.models.aluno import AlunoCreate, AlunoPublic, AlunoUpdate
from app.crud import aluno as crud


router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"]
)


#Cadastrar aluno
@router.post("/", response_model=AlunoPublic, status_code=201)
def criar_aluno(
    dados: AlunoCreate,
    session: Session = Depends(getSession),
):
    try:
        return crud.criar_aluno(dados, session)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Conflito de cadastro. Verifique o CPF e o e-mail"
        )


#Listar alunos
@router.get("/", response_model=list[AlunoPublic])
def listar_alunos(
    session: Session = Depends(getSession),
):
    return crud.listar_alunos(session)


#Buscar aluno por ID
@router.get("/{aluno_id}", response_model=AlunoPublic)
def buscar_aluno(
    aluno_id: int,
    session: Session = Depends(getSession),
):
    aluno = crud.buscar_aluno(aluno_id, session)

    if not aluno:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )

    return aluno


#Atualizar aluno
@router.patch("/{aluno_id}", response_model=AlunoPublic)
def atualizar_aluno(
    aluno_id: int,
    dados: AlunoUpdate,
    session: Session = Depends(getSession),
):
    try:
        aluno = crud.atualizar_aluno(
            aluno_id, dados, session
        )

        if not aluno:
            raise HTTPException(
                status_code=404,
                detail="Aluno não encontrado"
            )

        return aluno

    except ValidationError:
        raise HTTPException(
            status_code=422,
            detail="Dados inválidos para atualização do aluno"
        )

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Conflito na atualização. Verifique os dados do aluno"
        )


#Excluir aluno
@router.delete("/{aluno_id}", status_code=204)
def excluir_aluno(
    aluno_id: int,
    session: Session = Depends(getSession),
):
    try:
        excluido = crud.excluir_aluno(aluno_id, session)

        if not excluido:
            raise HTTPException(
                status_code=404,
                detail="Aluno não encontrado"
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
            detail="Aluno possui vínculo e não pode ser removido"
        )