from fastapi import HTTPException
from sqlmodel import Session

from app.models.matricula import Matricula, MatriculaStatus
from app.models.certificado import Certificado


# Emitir certificado
def emitir_certificado(matricula_id: int, session: Session):

    matricula = session.get(Matricula, matricula_id)

    if not matricula:
        raise HTTPException(
            status_code=404,
            detail="Matrícula não encontrada"
        )

    if matricula.status != MatriculaStatus.APROVADA:
        raise HTTPException(
            status_code=400,
            detail="A matrícula não está aprovada"
        )

    if matricula.certificado:
        raise HTTPException(
            status_code=409,
            detail="A matrícula já possui um certificado"
        )

    certificado = Certificado(
        matricula_id=matricula.id,
        codigo_validacao=f"CERT-{matricula.id}"
    )

    session.add(certificado)
    session.commit()
    session.refresh(certificado)

    return certificado


# Consultar certificado
def consultar_certificado(matricula_id: int, session: Session):

    matricula = session.get(Matricula, matricula_id)

    if not matricula:
        raise HTTPException(
            status_code=404,
            detail="Matrícula não encontrada"
        )

    if not matricula.certificado:
        raise HTTPException(
            status_code=404,
            detail="Certificado não encontrado"
        )

    return matricula.certificado