from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.turma import Turma
from app.models.aula import Aula, AulaCreate, AulaUpdate


def buscar_turma(turma_id: int, session: Session):
    turma = session.get(Turma, turma_id)

    if not turma:
        raise HTTPException(
            status_code=404,
            detail="Turma não encontrada."
        )

    return turma


def validar_periodo(dados: AulaCreate, turma: Turma):
    if not (turma.data_inicio <= dados.data <= turma.data_fim):
        raise ValueError(
            "A data da aula deve estar dentro do período da turma "
            f"({turma.data_inicio} a {turma.data_fim})"
        )


def criar_aula(dados: AulaCreate, session: Session):
    turma = buscar_turma(dados.turma_id, session)
    validar_periodo(dados, turma)
    aula = Aula.model_validate(dados)
    session.add(aula)
    session.commit()
    session.refresh(aula)
    return aula


# listar aulas (pode filtrar por turma)
def listar_aulas(session: Session, turma_id: int | None = None):
    consulta = select(Aula)

    if turma_id is not None:
        consulta = consulta.where(Aula.turma_id == turma_id)

    consulta = consulta.order_by(Aula.data, Aula.horario)
    aulas = session.exec(consulta).all()

    return aulas


#Buscar aula por ID
def buscar_aula(aula_id: int, session: Session):
    aula = session.get(Aula, aula_id)

    return aula


#Atualizar aula
def atualizar_aula(
    aula_id: int,
    dados: AulaUpdate,
    session: Session
):
    aula = buscar_aula(aula_id, session)

    if not aula:
        return None

    dados_atualizacao = dados.model_dump(exclude_unset=True)

    dados_validados = AulaCreate.model_validate({
        **aula.model_dump(),
        **dados_atualizacao
    })

    validar_periodo(dados_validados, aula.turma)

    aula.sqlmodel_update(dados_atualizacao)

    session.add(aula)
    session.commit()
    session.refresh(aula)

    return aula


#Excluir aula
def excluir_aula(aula_id: int, session: Session):
    aula = buscar_aula(aula_id, session)

    if not aula:
        return False

    if aula.frequencias:
        raise ValueError("Aula possui frequência registrada e não pode ser removida")

    session.delete(aula)
    session.commit()

    return True
