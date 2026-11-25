from sqlmodel import Session, select
from app.models.instrutor import Instrutor, InstrutorCreate, InstrutorUpdate

def criar_instrutor(dados: InstrutorCreate, session: Session):
    instrutor = Instrutor.model_validate(dados)
    session.add(instrutor)
    session.commit()
    session.refresh(instrutor)
    return instrutor

def listar_instrutores(session: Session):
    consulta = select(Instrutor)
    return session.exec(consulta).all()

def buscar_instrutor(instrutor_id: int, session: Session):
    return session.get(Instrutor, instrutor_id)

def atualizar_instrutor(instrutor_id: int, dados: InstrutorUpdate, session: Session):
    instrutor = buscar_instrutor(instrutor_id, session)
    if not instrutor:
        return None

    dados_atualizacao = dados.model_dump(exclude_unset=True)
    InstrutorCreate.model_validate({**instrutor.model_dump(), **dados_atualizacao})

    instrutor.sqlmodel_update(dados_atualizacao)
    session.add(instrutor)
    session.commit()
    session.refresh(instrutor)
    return instrutor

def excluir_instrutor(instrutor_id: int, session: Session):
    instrutor = buscar_instrutor(instrutor_id, session)
    if not instrutor:
        return False

    if instrutor.turmas:
        raise ValueError("Instrutor possui turmas associadas e não pode ser removido")

    session.delete(instrutor)
    session.commit()
    return True