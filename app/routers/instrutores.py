from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.database import getSession
from app.models.instrutor import InstrutorCreate, InstrutorPublic, InstrutorUpdate
from app.crud import instrutor as crud

router = APIRouter(prefix="/instrutores", tags=["Instrutores"])

@router.post("/", response_model=InstrutorPublic, status_code=201)
def criar_instrutor(dados: InstrutorCreate, session: Session = Depends(getSession)):
    try:
        return crud.criar_instrutor(dados, session)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Já existe um instrutor com esse CPF ou e-mail")

@router.get("/", response_model=list[InstrutorPublic])
def listar_instrutores(session: Session = Depends(getSession)):
    return crud.listar_instrutores(session)

@router.get("/{instrutor_id}", response_model=InstrutorPublic)
def buscar_instrutor(instrutor_id: int, session: Session = Depends(getSession)):
    instrutor = crud.buscar_instrutor(instrutor_id, session)
    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")
    return instrutor

@router.patch("/{instrutor_id}", response_model=InstrutorPublic)
def atualizar_instrutor(instrutor_id: int, dados: InstrutorUpdate, session: Session = Depends(getSession)):
    try:
        instrutor = crud.atualizar_instrutor(instrutor_id, dados, session)
        if not instrutor:
            raise HTTPException(status_code=404, detail="Instrutor não encontrado")
        return instrutor
    except ValidationError:
        raise HTTPException(status_code=422, detail="Dados inválidos para atualização do instrutor")
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Já existe um instrutor com esse CPF ou e-mail")

@router.delete("/{instrutor_id}", status_code=204)
def excluir_instrutor(instrutor_id: int, session: Session = Depends(getSession)):
    try:
        excluido = crud.excluir_instrutor(instrutor_id, session)
        if not excluido:
            raise HTTPException(status_code=404, detail="Instrutor não encontrado")
    except ValueError as erro:
        raise HTTPException(status_code=409, detail=str(erro))
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Instrutor possui vínculos e não pode ser removido")