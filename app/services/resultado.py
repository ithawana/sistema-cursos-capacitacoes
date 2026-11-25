from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.matricula import Matricula, MatriculaStatus
from app.models.avaliacao import Avaliacao
from app.models.resultado import (
    ResultadoAvaliacao,
    ResultadoAvaliacaoCreate
)


def registrar_resultado(dados: ResultadoAvaliacaoCreate, session: Session):

    matricula = session.get(Matricula, dados.matricula_id)
    avaliacao = session.get(Avaliacao, dados.avaliacao_id)

    if not matricula:
        raise HTTPException(
            status_code=404,
            detail="Matrícula não encontrada"
        )

    if not avaliacao:
        raise HTTPException(
            status_code=404,
            detail="Avaliação não encontrada"
        )

    if matricula.turma_id != avaliacao.turma_id:
        raise HTTPException(
            status_code=400,
            detail="A avaliação não pertence à turma da matrícula"
        )

    if matricula.status != MatriculaStatus.ATIVA:
        raise HTTPException(
            status_code=400,
            detail="A matrícula não está ativa"
        )

    if dados.nota > avaliacao.nota_maxima:
        raise HTTPException(
            status_code=400,
            detail="A nota ultrapassa a nota máxima da avaliação"
        )

    conflito = session.exec(
        select(ResultadoAvaliacao).where(
            ResultadoAvaliacao.matricula_id == dados.matricula_id,
            ResultadoAvaliacao.avaliacao_id == dados.avaliacao_id
        )
    ).first()

    if conflito:
        raise HTTPException(
            status_code=409,
            detail="Já existe uma nota registrada nesta avaliação"
        )

    resultado = ResultadoAvaliacao.model_validate(dados)

    session.add(resultado)
    session.commit()
    session.refresh(resultado)

    return resultado