from datetime import date

from fastapi import HTTPException
from sqlalchemy import and_
from sqlmodel import Session, select, func, col

from app.models.aluno import Aluno
from app.models.aula import Aula
from app.models.avaliacao import Avaliacao
from app.models.curso import Curso
from app.models.instrutor import Instrutor
from app.models.matricula import Matricula, MatriculaStatus
from app.models.matricula_aula import Matricula_Aula, FrequenciaStatus
from app.models.resultado import ResultadoAvaliacao
from app.models.turma import Turma


def buscar(modelo, id: int, nome: str, session: Session):
    objeto = session.get(modelo, id)

    if not objeto:
        raise HTTPException(
            status_code=404,
            detail=f"{nome} não encontrado(a)."
        )

    return objeto


# Converte as linhas do resultado em dicionários
def linhas_para_dict(resultado):
    return [dict(linha._mapping) for linha in resultado]


# 1) Situação dos participantes de uma turma (cursando, abandonou, cancelou, concluiu ou reprovou)
def participantes_turma(
    session: Session,
    turma_id: int,
    status: MatriculaStatus | None = None
):
    buscar(Turma, turma_id, "Turma", session)

    consulta = (
        select(
            Matricula.id.label("matricula_id"),
            Aluno.id.label("aluno_id"),
            Aluno.nome.label("aluno_nome"),
            Aluno.email.label("aluno_email"),
            Matricula.status,
            Matricula.data_matricula,
            Matricula.data_cancelamento,
        )
        .join(Aluno, Aluno.id == Matricula.aluno_id)
        .where(Matricula.turma_id == turma_id)
        .order_by(Aluno.nome)
    )

    if status:
        consulta = consulta.where(Matricula.status == status)

    return linhas_para_dict(session.exec(consulta))


# 2) Histórico de capacitações de um aluno (matricula, turma, curso, instrutor)
def historico_aluno(session: Session, aluno_id: int):
    buscar(Aluno, aluno_id, "Aluno", session)

    consulta = (
        select(
            Matricula.id.label("matricula_id"),
            Curso.id.label("curso_id"),
            Curso.nome.label("curso_nome"),
            Curso.carga_horaria,
            Turma.id.label("turma_id"),
            Turma.data_inicio.label("turma_data_inicio"),
            Turma.data_fim.label("turma_data_fim"),
            Instrutor.nome.label("instrutor_nome"),
            Matricula.status,
            Matricula.data_matricula,
        )
        .join(Turma, Turma.id == Matricula.turma_id)
        .join(Curso, Curso.id == Turma.curso_id)
        .join(Instrutor, Instrutor.id == Turma.instrutor_id)
        .where(Matricula.aluno_id == aluno_id)
        .order_by(col(Turma.data_inicio).desc())
    )

    return linhas_para_dict(session.exec(consulta))


# 3) Matrículas por situação: quem abandonou, cancelou ou ainda está cursando
def matriculas_por_situacao(
    session: Session,
    status: MatriculaStatus,
    curso_id: int | None = None,
    turma_id: int | None = None,
):
    consulta = (
        select(
            Matricula.id.label("matricula_id"),
            Matricula.status,
            Matricula.data_matricula,
            Matricula.data_cancelamento,
            Aluno.id.label("aluno_id"),
            Aluno.nome.label("aluno_nome"),
            Turma.id.label("turma_id"),
            Curso.id.label("curso_id"),
            Curso.nome.label("curso_nome"),
        )
        .join(Aluno, Aluno.id == Matricula.aluno_id)
        .join(Turma, Turma.id == Matricula.turma_id)
        .join(Curso, Curso.id == Turma.curso_id)
        .where(Matricula.status == status)
        .order_by(Curso.nome, Aluno.nome)
    )

    if curso_id is not None:
        consulta = consulta.where(Curso.id == curso_id)

    if turma_id is not None:
        consulta = consulta.where(Turma.id == turma_id)

    return linhas_para_dict(session.exec(consulta))


# CONSULTAS COMPLEXAS
# 4) Cursos com maior quantidade de concluintes (join, count, group by, order by) 
def cursos_mais_concluintes(
    session: Session,
    limite: int = 5,
    data_de: date | None = None, # filtra de xx/xx/xxxx até xx/xx/xxxx
    data_ate: date | None = None,
):
    total_concluintes = func.count(Matricula.id).label("total_concluintes")

    consulta = (
        select(
            Curso.id.label("curso_id"),
            Curso.nome.label("curso_nome"),
            total_concluintes,
        )
        .join(Turma, Turma.curso_id == Curso.id)
        .join(Matricula, Matricula.turma_id == Turma.id)
        .where(Matricula.status == MatriculaStatus.APROVADA)
    )

    # Período considerado pela data de término da turma
    if data_de:
        consulta = consulta.where(Turma.data_fim >= data_de)

    if data_ate:
        consulta = consulta.where(Turma.data_fim <= data_ate)

    consulta = (
        consulta
        .group_by(Curso.id, Curso.nome)
        .order_by(total_concluintes.desc(), Curso.nome)
        .limit(limite)
    )

    return linhas_para_dict(session.exec(consulta))


# 5) Frequência dos alunos 
# left join, group by, having
def frequencia_turma(
    session: Session,
    turma_id: int,
    apenas_abaixo_minimo: bool = False,
):
    turma = buscar(Turma, turma_id, "Turma", session)
    hoje = date.today()

    aulas_realizadas = session.exec( # até hoje
        select(func.count(Aula.id))
        .where(Aula.turma_id == turma_id, Aula.data <= hoje)
    ).one()

    # Conta Aula.id para considerar só presenças em aulas já realizadas
    presencas = func.count(Aula.id).label("presencas")

    consulta = (
        select(
            Matricula.id.label("matricula_id"),
            Aluno.id.label("aluno_id"),
            Aluno.nome.label("aluno_nome"),
            Matricula.status,
            presencas,
        )
        .join(Aluno, Aluno.id == Matricula.aluno_id)
        .outerjoin(Matricula_Aula, and_( # == LEFT JOIN, and_ == AND dentro do ON
            Matricula_Aula.matricula_id == Matricula.id,
            Matricula_Aula.frequencia == FrequenciaStatus.PRESENTE,
        ))
        .outerjoin(Aula, and_( # == LEFT JOIN, and_ == AND dentro do ON
            Aula.id == Matricula_Aula.aula_id,
            Aula.data <= hoje,
        ))
        .where(
            Matricula.turma_id == turma_id,
            Matricula.status != MatriculaStatus.CANCELADA,
        )
        .group_by(Matricula.id, Aluno.id, Aluno.nome, Matricula.status)
        .order_by(Aluno.nome)
    )

    if apenas_abaixo_minimo:
        if aulas_realizadas == 0:
            return []

        consulta = consulta.having( # filtra o grupo que ficou com menos de 75%
            presencas * 100.0 / aulas_realizadas < turma.frequencia_minima
        )

    resultado = []

    for linha in session.exec(consulta):
        dados = dict(linha._mapping)

        if aulas_realizadas > 0:
            percentual = round(dados["presencas"] * 100 / aulas_realizadas, 2)
        else:
            percentual = None

        dados.update({
            "aulas_realizadas": aulas_realizadas,
            "percentual_frequencia": percentual,
            "frequencia_minima": turma.frequencia_minima,
            "abaixo_do_minimo": percentual is not None and percentual < turma.frequencia_minima,
        })
        resultado.append(dados)

    return resultado


# ESTATÍSTICAS
def estatisticas(session: Session):
    def status_zerados():
        return {
            "ATIVA": 0,
            "INATIVA": 0,
            "CANCELADA": 0,
            "ABANDONADA": 0,
            "APROVADA": 0,
            "REPROVADA": 0,
        }

    # Totais simples (COUNT)
    total_alunos = session.exec(select(func.count(Aluno.id))).one()
    total_cursos = session.exec(select(func.count(Curso.id))).one()
    total_turmas = session.exec(select(func.count(Turma.id))).one()

    # Matrículas por status (COUNT + GROUP BY)
    por_status = status_zerados()
    for status, quantidade in session.exec(
        select(Matricula.status, func.count(Matricula.id))
        .group_by(Matricula.status)
    ):
        por_status[MatriculaStatus(status).value] = quantidade

    # Quantidade de turmas por curso (LEFT JOIN para incluir cursos sem turma)
    cursos = {}
    for curso_id, curso_nome, qtd_turmas in session.exec(
        select(Curso.id, Curso.nome, func.count(Turma.id))
        .outerjoin(Turma, Turma.curso_id == Curso.id) # LEFT JOIN
        .group_by(Curso.id, Curso.nome)
        .order_by(Curso.nome)
    ):
        cursos[curso_id] = {
            "curso_id": curso_id,
            "curso_nome": curso_nome,
            "total_turmas": qtd_turmas,
            "total_matriculas": 0,
            "matriculas_por_status": status_zerados(),
            "taxa_aprovacao": None,
            "media_notas": None,
        }

    # Matrículas por curso e por status (COUNT + GROUP BY em duas colunas)
    for curso_id, status, quantidade in session.exec(
        select(Turma.curso_id, Matricula.status, func.count(Matricula.id))
        .join(Matricula, Matricula.turma_id == Turma.id)
        .group_by(Turma.curso_id, Matricula.status)
    ):
        cursos[curso_id]["matriculas_por_status"][MatriculaStatus(status).value] = quantidade
        cursos[curso_id]["total_matriculas"] += quantidade

    # Média das notas por curso (AVG + GROUP BY)
    for curso_id, media in session.exec(
        select(Turma.curso_id, func.avg(ResultadoAvaliacao.nota))
        .join(Avaliacao, Avaliacao.id == ResultadoAvaliacao.avaliacao_id)
        .join(Turma, Turma.id == Avaliacao.turma_id)
        .group_by(Turma.curso_id)
    ):
        cursos[curso_id]["media_notas"] = round(float(media), 2)

    # Taxa de aprovação = aprovadas / (aprovadas + reprovadas)
    for curso in cursos.values():
        aprovadas = curso["matriculas_por_status"][MatriculaStatus.APROVADA.value]
        reprovadas = curso["matriculas_por_status"][MatriculaStatus.REPROVADA.value]

        if aprovadas + reprovadas > 0:
            curso["taxa_aprovacao"] = round(aprovadas * 100 / (aprovadas + reprovadas), 2)

    return {
        "total_alunos": total_alunos,
        "total_cursos": total_cursos,
        "total_turmas": total_turmas,
        "matriculas_por_status": por_status,
        "cursos": list(cursos.values()),
    }
