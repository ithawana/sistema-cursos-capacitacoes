from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.turma import Turma
from app.models.avaliacao import Avaliacao, AvaliacaoCreate, AvaliacaoUpdate


def buscar_turma(turma_id: int, session: Session):
    turma = session.get(Turma, turma_id)

    if not turma:
        raise HTTPException(
            status_code=404,
            detail="Turma não encontrada."
        )

    return turma


# A avaliação deve acontecer dentro do período de realização da turma
def validar_periodo(dados: AvaliacaoCreate, turma: Turma):
    if not (turma.data_inicio <= dados.data <= turma.data_fim):
        raise ValueError(
            "A data da avaliação deve estar dentro do período da turma "
            f"({turma.data_inicio} a {turma.data_fim})"
        )


#Cadastrar avaliacao
def criar_avaliacao(dados: AvaliacaoCreate, session: Session):
    turma = buscar_turma(dados.turma_id, session)

    validar_periodo(dados, turma)

    avaliacao = Avaliacao.model_validate(dados)

    session.add(avaliacao)
    session.commit()
    session.refresh(avaliacao)

    return avaliacao


#Listar avaliacoes (opcionalmente filtrando por turma)
def listar_avaliacoes(session: Session, turma_id: int | None = None):
    consulta = select(Avaliacao)

    if turma_id is not None:
        consulta = consulta.where(Avaliacao.turma_id == turma_id)

    consulta = consulta.order_by(Avaliacao.data)
    avaliacoes = session.exec(consulta).all()

    return avaliacoes


#Buscar avaliacao por ID
def buscar_avaliacao(avaliacao_id: int, session: Session):
    avaliacao = session.get(Avaliacao, avaliacao_id)

    return avaliacao


#Atualizar avaliacao
def atualizar_avaliacao(
    avaliacao_id: int,
    dados: AvaliacaoUpdate,
    session: Session
):
    avaliacao = buscar_avaliacao(avaliacao_id, session)

    if not avaliacao:
        return None

    dados_atualizacao = dados.model_dump(exclude_unset=True)

    dados_validados = AvaliacaoCreate.model_validate({
        **avaliacao.model_dump(),
        **dados_atualizacao
    })

    validar_periodo(dados_validados, avaliacao.turma)

    # A nota máxima não pode ficar abaixo de notas já lançadas
    maior_nota = max(
        (resultado.nota for resultado in avaliacao.resultados),
        default=None
    )

    if maior_nota is not None and dados_validados.nota_maxima < maior_nota:
        raise ValueError(
            "A nota máxima não pode ser menor que uma nota já lançada "
            f"nesta avaliação ({maior_nota})"
        )

    avaliacao.sqlmodel_update(dados_atualizacao)

    session.add(avaliacao)
    session.commit()
    session.refresh(avaliacao)

    return avaliacao


#Excluir avaliacao
def excluir_avaliacao(avaliacao_id: int, session: Session):
    avaliacao = buscar_avaliacao(avaliacao_id, session)

    if not avaliacao:
        return False

    if avaliacao.resultados:
        raise ValueError("Avaliação possui resultados lançados e não pode ser removida")

    session.delete(avaliacao)
    session.commit()

    return True
