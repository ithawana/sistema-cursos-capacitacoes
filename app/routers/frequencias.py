from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.database import getSession
from app.models.matricula_aula import (
    MatriculaAulaCreate,
    MatriculaAulaPublic
)
from app.services import frequencia as service


router = APIRouter(
    prefix="/frequencias",
    tags=["Frequencias"]
)


#Registrar frequência
@router.post("/", response_model=MatriculaAulaPublic, status_code=201)
def registrar_frequencia(
    dados: MatriculaAulaCreate,
    session: Session = Depends(getSession)
):
    try:
        return service.registrar_frequencia(dados, session)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Conflito no registro da frequência"
        )