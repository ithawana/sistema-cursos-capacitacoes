from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.database import getSession
from app.models.resultado import (
    ResultadoAvaliacaoCreate,
    ResultadoAvaliacaoPublic
)
from app.services import resultado as service


router = APIRouter(
    prefix="/resultados-avaliacao",
    tags=["Resultados das Avaliações"]
)


@router.post("/", response_model=ResultadoAvaliacaoPublic, status_code=201)
def registrar_resultado(
    dados: ResultadoAvaliacaoCreate,
    session: Session = Depends(getSession)
):
    try:
        return service.registrar_resultado(dados, session)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Conflito no registro do resultado"
        )