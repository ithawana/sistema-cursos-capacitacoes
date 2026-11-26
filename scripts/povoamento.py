from datetime import date, time, timedelta
from sqlmodel import Session, select

from app.database import engine

from app.models.aluno import Aluno, AlunoCreate
from app.models.instrutor import Instrutor, InstrutorCreate
from app.models.curso import Curso, CursoCreate
from app.models.turma import Turma, TurmaCreate
from app.models.matricula import (Matricula, MatriculaCreate, MatriculaUpdate, MatriculaStatus)

from app.models.aula import Aula, AulaCreate
from app.models.avaliacao import Avaliacao, AvaliacaoCreate
from app.models.matricula_aula import (Matricula_Aula, MatriculaAulaCreate, FrequenciaStatus)

from app.models.resultado import (ResultadoAvaliacao, ResultadoAvaliacaoCreate)

from app.crud.aluno import criar_aluno
from app.crud.instrutor import criar_instrutor
from app.crud.curso import criar_curso
from app.crud.turma import criar_turma
from app.crud.matricula import (criar_matricula, atualizar_matricula, cancelar_matricula)

from app.crud.aula import criar_aula
from app.crud.avaliacao import criar_avaliacao

from app.services.frequencia import registrar_frequencia
from app.services.resultado import registrar_resultado
from app.services.conclusao import finalizar_matricula

def povoar_alunos(session: Session):
    nomes = [
        "Ana Silva",
        "Bruno Santos",
        "Camila Oliveira",
        "Daniel Souza",
        "Eduarda Lima",
        "Felipe Costa",
        "Gabriela Alves",
        "Henrique Rocha",
        "Isabela Martins",
        "João Ferreira",
        "Larissa Gomes",
        "Marcos Ribeiro"
    ]

    alunos = []

    for i, nome in enumerate(nomes, start=1):

        dados = AlunoCreate(
            nome=nome,
            cpf=f"{i:011d}",
            email=f"aluno{i}@example.com",
            data_nascimento=date(2003, 5, 10)
        )

        aluno = criar_aluno(dados, session)

        alunos.append(aluno)

    return alunos

def povoar_instrutores(session: Session):
    instrutor1 = criar_instrutor(
        InstrutorCreate(
            nome="Carlos Mendes",
            cpf="00000000101",
            email="carlos@example.com",
            data_nascimento=date(1985, 3, 15)
        ),
        session
    )

    instrutor2 = criar_instrutor(
        InstrutorCreate(
            nome="Mariana Almeida",
            cpf="00000000102",
            email="mariana@example.com",
            data_nascimento=date(1990, 7, 20)
        ),
        session
    )

    return [instrutor1, instrutor2]

def povoar_cursos(session: Session):
    curso1 = criar_curso(
        CursoCreate(
            nome="Python Básico",
            objetivos="Aprender fundamentos de programação",
            conteudo_programatico="Variáveis, condições e funções",
            carga_horaria=8
        ),
        session
    )

    curso2 = criar_curso(
        CursoCreate(
            nome="Excel Básico",
            objetivos="Aprender a utilizar planilhas",
            conteudo_programatico="Fórmulas, tabelas e gráficos",
            carga_horaria=8
        ),
        session
    )

    return [curso1, curso2]

def povoar_turmas(cursos, instrutores, session: Session):
    hoje = date.today()

    turma1 = criar_turma(
        TurmaCreate(
            curso_id=cursos[0].id,
            instrutor_id=instrutores[0].id,
            numero_vagas=10,
            data_inicio=hoje - timedelta(days=30),
            data_fim=hoje - timedelta(days=10),
            frequencia_minima=75,
            nota_minima=7,
            modalidade="Presencial"
        ),
        session
    )

    turma2 = criar_turma(
        TurmaCreate(
            curso_id=cursos[1].id,
            instrutor_id=instrutores[1].id,
            numero_vagas=10,
            data_inicio=hoje - timedelta(days=20),
            data_fim=hoje - timedelta(days=2),
            frequencia_minima=75,
            nota_minima=7,
            modalidade="Online"
        ),
        session
    )

    turma3 = criar_turma(
        TurmaCreate(
            curso_id=cursos[0].id,
            instrutor_id=instrutores[0].id,
            numero_vagas=6,
            data_inicio=hoje - timedelta(days=5),
            data_fim=hoje + timedelta(days=5),
            frequencia_minima=80,
            nota_minima=8,
            modalidade="Presencial"
        ),
        session
    )

    return [turma1, turma2, turma3]

def povoar_matriculas(alunos, turmas, session: Session):
    matriculas = []

    grupos = [
        alunos[0:6],
        alunos[4:8],
        alunos[6:12]
    ]

    for turma, grupo in zip(turmas, grupos):

        for aluno in grupo:

            dados = MatriculaCreate(
                aluno_id=aluno.id,
                turma_id=turma.id,
                data_matricula=turma.data_inicio,
                status=MatriculaStatus.ATIVA
            )

            matricula = criar_matricula(dados, session)

            matriculas.append(matricula)

    return matriculas

def povoar_aulas(turmas, session: Session):
    aulas = []

    dias_por_turma = [
        [2, 4, 6, 8],
        [1, 4, 7, 10],
        [1, 3]
    ]

    for turma, dias in zip(turmas, dias_por_turma):

        for numero, dia in enumerate(dias, start=1):

            dados = AulaCreate(
                turma_id=turma.id,
                data=turma.data_inicio + timedelta(days=dia),
                horario=time(8, 0),
                duracao=120,
                conteudo=f"Conteúdo da aula {numero}"
            )

            aula = criar_aula(dados, session)

            aulas.append(aula)

    return aulas

def povoar_avaliacoes(turmas, session: Session):
    avaliacoes = []

    dias_por_turma = [
        [5, 9],
        [5, 12],
        [3]
    ]

    for turma, dias in zip(turmas, dias_por_turma):

        for numero, dia in enumerate(dias, start=1):

            dados = AvaliacaoCreate(
                turma_id=turma.id,
                titulo=f"Avaliação {numero}",
                data=turma.data_inicio + timedelta(days=dia),
                nota_maxima=10,
                peso=1
            )

            avaliacao = criar_avaliacao(dados, session)

            avaliacoes.append(avaliacao)

    return avaliacoes

def povoar_participacao(matriculas, aulas, avaliacoes, session: Session):
    hoje = date.today()

    for i, matricula in enumerate(matriculas):

        for aula in aulas:

            if aula.turma_id != matricula.turma_id:
                continue

            if aula.data > hoje:
                continue

            frequencia = FrequenciaStatus.PRESENTE

            if i % 4 == 1:
                frequencia = FrequenciaStatus.AUSENTE

            registrar_frequencia(
                MatriculaAulaCreate(
                    matricula_id=matricula.id,
                    aula_id=aula.id,
                    frequencia=frequencia
                ),
                session
            )

        for avaliacao in avaliacoes:

            if avaliacao.turma_id != matricula.turma_id:
                continue

            if avaliacao.data > hoje:
                continue

            nota = 8.5

            if i % 4 == 2:
                nota = 5.0

            registrar_resultado(
                ResultadoAvaliacaoCreate(
                    matricula_id=matricula.id,
                    avaliacao_id=avaliacao.id,
                    nota=nota
                ),
                session
            )

def povoar_conclusoes(matriculas, session: Session):
    hoje = date.today()

    for matricula in matriculas:

        if matricula.turma.data_fim <= hoje:

            finalizar_matricula(
                matricula.id,
                session
            )

    # Cancelar uma matrícula da turma em andamento
    cancelar_matricula(
        matriculas[10].id,
        session
    )

    # Registrar uma matrícula abandonada
    atualizar_matricula(
        matriculas[11].id,
        MatriculaUpdate(
            status=MatriculaStatus.ABANDONADA
        ),
        session
    )

def povoar_banco():
    with Session(engine) as session:

        # Verificar se o banco já possui registros
        if (
            session.exec(select(Aluno)).first()
            or session.exec(select(Instrutor)).first()
            or session.exec(select(Curso)).first()
            or session.exec(select(Turma)).first()
            or session.exec(select(Matricula)).first()
            or session.exec(select(Aula)).first()
            or session.exec(select(Avaliacao)).first()
            or session.exec(select(Matricula_Aula)).first()
            or session.exec(select(ResultadoAvaliacao)).first()
        ):
            print("O banco já possui registros. Utilize um banco vazio.")
            return

        alunos = povoar_alunos(session)

        instrutores = povoar_instrutores(session)

        cursos = povoar_cursos(session)

        turmas = povoar_turmas(
            cursos,
            instrutores,
            session
        )

        matriculas = povoar_matriculas(
            alunos,
            turmas,
            session
        )

        aulas = povoar_aulas(
            turmas,
            session
        )

        avaliacoes = povoar_avaliacoes(
            turmas,
            session
        )

        povoar_participacao(
            matriculas,
            aulas,
            avaliacoes,
            session
        )

        povoar_conclusoes(
            matriculas,
            session
        )

        print("Banco povoado com sucesso!")


if __name__ == "__main__":
    povoar_banco()