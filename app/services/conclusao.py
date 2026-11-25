from datetime import date
from fastapi import HTTPException
from sqlmodel import Session

from app.models.matricula import Matricula, MatriculaStatus
from app.models.matricula_aula import FrequenciaStatus


def consultar_progresso(matricula_id: int, session: Session):

    matricula = session.get(Matricula, matricula_id)

    if not matricula:
        raise HTTPException(
            status_code=404,
            detail="Matrícula não encontrada"
        )

    turma = matricula.turma
    hoje = date.today()

    # Calcular frequência
    total_aulas = 0
    presencas = 0
    frequencias_registradas = 0

    for aula in turma.aulas:
        if aula.data <= hoje:
            total_aulas += 1

    for registro in matricula.frequencias:
        if registro.aula.data <= hoje:
            frequencias_registradas += 1

            if registro.frequencia == FrequenciaStatus.PRESENTE:
                presencas += 1

    frequencia = None

    if total_aulas > 0:
        frequencia = presencas * 100 / total_aulas

    # Calcular média ponderada das notas
    soma_notas = 0
    soma_pesos = 0
    avaliacoes_registradas = 0

    for resultado in matricula.resultados_avaliacao:
        avaliacao = resultado.avaliacao

        if avaliacao.data <= hoje:
            nota = resultado.nota * 10 / avaliacao.nota_maxima

            soma_notas += nota * avaliacao.peso
            soma_pesos += avaliacao.peso
            avaliacoes_registradas += 1

    nota_final = None

    if soma_pesos > 0:
        nota_final = soma_notas / soma_pesos

    # Verificar se pode concluir
    situacao = matricula.status
    pode_finalizar = False

    if (
        matricula.status == MatriculaStatus.ATIVA
        and hoje >= turma.data_fim
        and total_aulas > 0
        and frequencias_registradas == total_aulas
        and avaliacoes_registradas == len(turma.avaliacoes)
    ):
        if turma.nota_minima is None or nota_final is not None:
            pode_finalizar = True

            if (
                frequencia >= turma.frequencia_minima
                and (
                    turma.nota_minima is None
                    or nota_final >= turma.nota_minima
                )
            ):
                situacao = MatriculaStatus.APROVADA
            else:
                situacao = MatriculaStatus.REPROVADA

    return {
        "matricula_id": matricula.id,
        "frequencia": round(frequencia, 2) if frequencia is not None else None,
        "nota_final": round(nota_final, 2) if nota_final is not None else None,
        "frequencia_minima": turma.frequencia_minima,
        "nota_minima": turma.nota_minima,
        "situacao": situacao,
        "pode_finalizar": pode_finalizar
    }