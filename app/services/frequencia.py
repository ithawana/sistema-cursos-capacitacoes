from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.matricula import Matricula, MatriculaStatus
from app.models.aula import Aula
from app.models.matricula_aula import (
    Matricula_Aula,
    MatriculaAulaCreate
)


def registrar_frequencia(dados: MatriculaAulaCreate, session: Session):

    matricula = session.get(Matricula, dados.matricula_id)
    aula = session.get(Aula, dados.aula_id)

    if not matricula:
        raise HTTPException(
            status_code=404,
            detail="Matrícula não encontrada"
        )

    if not aula:
        raise HTTPException(
            status_code=404,
            detail="Aula não encontrada"
        )

    if matricula.turma_id != aula.turma_id:
        raise HTTPException(
            status_code=400,
            detail="A aula não pertence à turma da matrícula"
        )

    if matricula.status != MatriculaStatus.ATIVA:
        raise HTTPException(
            status_code=400,
            detail="A matrícula não está ativa"
        )

    conflito = session.exec(
        select(Matricula_Aula).where(
            Matricula_Aula.matricula_id == dados.matricula_id,
            Matricula_Aula.aula_id == dados.aula_id
        )
    ).first()

    if conflito:
        raise HTTPException(
            status_code=409,
            detail="Frequência já registrada nesta aula"
        )

    frequencia = Matricula_Aula.model_validate(dados)
    frequencia.data_aula = aula.data

    session.add(frequencia)
    session.commit()
    session.refresh(frequencia)

    return frequencia