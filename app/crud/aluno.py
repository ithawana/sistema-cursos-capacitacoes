from sqlmodel import Session, select
from app.models.aluno import Aluno, AlunoCreate, AlunoUpdate


#Cadastrar aluno
def criar_aluno(dados: AlunoCreate, session: Session):
    aluno = Aluno.model_validate(dados)

    session.add(aluno)
    session.commit()
    session.refresh(aluno)

    return aluno


#Listar alunos com paginação e filtro
def listar_alunos(
    session: Session,
    page: int,
    size: int,
    nome: str | None = None
):
    consulta = select(Aluno)

    if nome:
        filtro_nome = Aluno.nome.ilike(f"%{nome}%")
        consulta = consulta.where(filtro_nome)

    offset = (page - 1) * size

    consulta = (
        consulta
        .order_by(Aluno.id)
        .offset(offset)
        .limit(size)
    )

    alunos = session.exec(consulta).all()

    return alunos


#Buscar aluno por ID
def buscar_aluno(aluno_id: int, session: Session):
    aluno = session.get(Aluno, aluno_id)

    return aluno


#Atualizar aluno
def atualizar_aluno(
    aluno_id: int,
    dados: AlunoUpdate,
    session: Session
):
    aluno = buscar_aluno(aluno_id, session)

    if not aluno:
        return None

    dados_atualizacao = dados.model_dump(exclude_unset=True)

    AlunoCreate.model_validate({
        **aluno.model_dump(),
        **dados_atualizacao
    })

    aluno.sqlmodel_update(dados_atualizacao)

    session.add(aluno)
    session.commit()
    session.refresh(aluno)

    return aluno


#Excluir aluno
def excluir_aluno(aluno_id: int, session: Session):
    aluno = buscar_aluno(aluno_id, session)

    if not aluno:
        return False

    if aluno.matriculas:
        raise ValueError("Aluno possui matrícula associada")

    session.delete(aluno)
    session.commit()

    return True
