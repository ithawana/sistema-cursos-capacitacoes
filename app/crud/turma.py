from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.turma import Turma, TurmaCreate, TurmaUpdate
from app.models.curso import Curso
from app.models.instrutor import Instrutor

def validar_referencias(curso_id: int, instrutor_id: int, session: Session):
    if not session.get(Curso, curso_id):
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    if not session.get(Instrutor, instrutor_id):
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")

def validar_periodo(data_inicio, data_fim):
    if data_fim < data_inicio:
        raise ValueError("A data de término não pode ser anterior à data de início")

def criar_turma(dados: TurmaCreate, session: Session):
    validar_referencias(dados.curso_id, dados.instrutor_id, session)
    validar_periodo(dados.data_inicio, dados.data_fim)

    turma = Turma.model_validate(dados)
    session.add(turma)
    session.commit()
    session.refresh(turma)
    return turma

def listar_turmas(session: Session):
    consulta = select(Turma)
    return session.exec(consulta).all()

def buscar_turma(turma_id: int, session: Session):
    return session.get(Turma, turma_id)

def atualizar_turma(turma_id: int, dados: TurmaUpdate, session: Session):
    turma = buscar_turma(turma_id, session)
    if not turma:
        return None

    dados_atualizacao = dados.model_dump(exclude_unset=True)
    dados_completos = {**turma.model_dump(), **dados_atualizacao}
    dados_validados = TurmaCreate.model_validate(dados_completos)

    validar_referencias(dados_validados.curso_id, dados_validados.instrutor_id, session)
    validar_periodo(dados_validados.data_inicio, dados_validados.data_fim)

    turma.sqlmodel_update(dados_atualizacao)
    session.add(turma)
    session.commit()
    session.refresh(turma)
    return turma

def excluir_turma(turma_id: int, session: Session):
    turma = buscar_turma(turma_id, session)
    if not turma:
        return False

    if turma.aulas or turma.matriculas or turma.avaliacoes:
        raise ValueError("Turma possui aulas, matrículas ou avaliações associadas e não pode ser removida")

    session.delete(turma)
    session.commit()
    return True