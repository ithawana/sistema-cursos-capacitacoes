from sqlmodel import Session, select
from app.models.curso import Curso, CursoCreate, CursoUpdate

def criar_curso(dados: CursoCreate, session: Session):
    curso = Curso.model_validate(dados)
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso

def listar_cursos(session: Session):
    consulta = select(Curso)
    return session.exec(consulta).all()

def buscar_curso(curso_id: int, session: Session):
    return session.get(Curso, curso_id)

def atualizar_curso(curso_id: int, dados: CursoUpdate, session: Session):
    curso = buscar_curso(curso_id, session)
    if not curso:
        return None

    dados_atualizacao = dados.model_dump(exclude_unset=True)

    CursoCreate.model_validate({**curso.model_dump(), **dados_atualizacao})

    curso.sqlmodel_update(dados_atualizacao)
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso

def excluir_curso(curso_id: int, session: Session):
    curso = buscar_curso(curso_id, session)
    if not curso:
        return False

    if curso.turmas:
        raise ValueError("Curso possui turmas associadas e não pode ser removido")

    session.delete(curso)
    session.commit()
    return True
