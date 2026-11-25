from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.database import getSession
from app.models.curso import CursoCreate, CursoPublic, CursoUpdate
from app.crud import curso as crud

router = APIRouter(prefix="/cursos", tags=["Cursos"])

@router.post("/", response_model=CursoPublic, status_code=201)
def criar_curso(dados: CursoCreate, session: Session = Depends(getSession)):
    try:
        return crud.criar_curso(dados, session)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Já existe um curso com esse nome")

@router.get("/", response_model=list[CursoPublic])
def listar_cursos(session: Session = Depends(getSession)):
    return crud.listar_cursos(session)

@router.get("/{curso_id}", response_model=CursoPublic)
def buscar_curso(curso_id: int, session: Session = Depends(getSession)):
    curso = crud.buscar_curso(curso_id, session)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return curso

@router.patch("/{curso_id}", response_model=CursoPublic)
def atualizar_curso(curso_id: int, dados: CursoUpdate, session: Session = Depends(getSession)):
    try:
        curso = crud.atualizar_curso(curso_id, dados, session)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso não encontrado")
        return curso
    except ValidationError:
        raise HTTPException(status_code=422, detail="Dados inválidos para atualização do curso")
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Já existe um curso com esse nome")

@router.delete("/{curso_id}", status_code=204)
def excluir_curso(curso_id: int, session: Session = Depends(getSession)):
    try:
        excluido = crud.excluir_curso(curso_id, session)
        if not excluido:
            raise HTTPException(status_code=404, detail="Curso não encontrado")
    except ValueError as erro:
        raise HTTPException(status_code=409, detail=str(erro))
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Curso possui vínculos e não pode ser removido")
