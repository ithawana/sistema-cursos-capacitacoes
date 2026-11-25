from datetime import date
from sqlmodel import Session, select
from fastapi import HTTPException
from sqlalchemy import func

from app.models.aluno import Aluno
from app.models.turma import Turma
from app.models.matricula import (
    Matricula,
    MatriculaCreate,
    MatriculaUpdate,
    MatriculaStatus
)


def validar_referencias(
    aluno_id: int,
    turma_id: int,
    session: Session
):
    aluno = session.get(Aluno, aluno_id)

    if not aluno:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado."
        )

    turma = session.get(Turma, turma_id)

    if not turma:
        raise HTTPException(
            status_code=404,
            detail="Turma não encontrada."
        )

    return turma

def validar_vagas(turma: Turma, session: Session):
    consulta = select(func.count()).select_from(Matricula).where(
        Matricula.turma_id == turma.id,
        Matricula.status == MatriculaStatus.ATIVA
    )

    total_matriculas = session.exec(consulta).one()

    if total_matriculas >= turma.numero_vagas:
        raise HTTPException(
            status_code=409,
            detail="A turma atingiu o limite de vagas."
        )


#Cadastrar matricula
def criar_matricula(dados: MatriculaCreate, session: Session):
    turma = validar_referencias(
        dados.aluno_id,
        dados.turma_id,
        session
    )

    if dados.status != MatriculaStatus.ATIVA:
        raise ValueError("A matrícula deve iniciar como ativa")

    if dados.data_cancelamento is not None:
        raise ValueError("Uma nova matrícula não pode possuir data de cancelamento")

    if dados.data_matricula > date.today():
        raise ValueError("A data da matrícula não pode ser futura")

    # Verifica matrícula duplicada
    conflito = session.exec(
        select(Matricula).where(
            Matricula.aluno_id == dados.aluno_id,
            Matricula.turma_id == dados.turma_id
        )
    ).first()

    if conflito:
        raise HTTPException(
            status_code=409,
            detail="O aluno já possui matrícula nesta turma"
        )

    # Verifica disponibilidade de vagas
    validar_vagas(turma, session)

    matricula = Matricula.model_validate(dados)

    session.add(matricula)
    session.commit()
    session.refresh(matricula)

    return matricula


#Listar matriculas
def listar_matriculas(session: Session):
    consulta = select(Matricula)
    matriculas = session.exec(consulta).all()

    return matriculas


#Buscar matricula por ID
def buscar_matricula(matricula_id: int, session: Session):
    matricula = session.get(Matricula, matricula_id)

    return matricula


#Atualizar matricula
def atualizar_matricula(
    matricula_id: int,
    dados: MatriculaUpdate,
    session: Session
):
    matricula = buscar_matricula(matricula_id, session)

    if not matricula:
        return None

    dados_atualizacao = dados.model_dump(exclude_unset=True)

    dados_validados = MatriculaCreate.model_validate({
        **matricula.model_dump(),
        **dados_atualizacao
    })

    if matricula.status in (
        MatriculaStatus.CANCELADA,
        MatriculaStatus.APROVADA,
        MatriculaStatus.REPROVADA
    ):
        raise ValueError("Uma matrícula cancelada ou concluída não pode ser alterada")

    if dados_validados.status in (
        MatriculaStatus.APROVADA,
        MatriculaStatus.REPROVADA
    ):
        raise ValueError("A situação de conclusão deve ser determinada pelo sistema")

    if dados_validados.status == MatriculaStatus.CANCELADA:
        raise ValueError("Utilize a operação de cancelamento da matrícula")

    if dados_validados.data_cancelamento is not None:
        raise ValueError("A data de cancelamento deve ser definida pelo sistema")

    if dados_validados.data_matricula > date.today():
        raise ValueError("A data da matrícula não pode ser futura")

    if (
        matricula.status != MatriculaStatus.ATIVA
        and dados_validados.status == MatriculaStatus.ATIVA
    ):
        validar_vagas(matricula.turma, session)

    matricula.sqlmodel_update(dados_atualizacao)

    session.add(matricula)
    session.commit()
    session.refresh(matricula)

    return matricula


#Cancelar matricula
def cancelar_matricula(matricula_id: int, session: Session):
    matricula = buscar_matricula(matricula_id, session)

    if not matricula:
        return False

    if matricula.status == MatriculaStatus.CANCELADA:
        return True

    if matricula.status in (
        MatriculaStatus.APROVADA,
        MatriculaStatus.REPROVADA
    ):
        raise ValueError("Matrícula concluída não pode ser cancelada")

    matricula.status = MatriculaStatus.CANCELADA
    matricula.data_cancelamento = date.today()

    session.add(matricula)
    session.commit()
    return True