# Evolução do esquema com Alembic

## Alteração realizada

Foi adicionado o atributo `modalidade` à entidade `Turma`:
- Tipo: texto com até 20 caracteres;
- Obrigatório;
- Valor padrão: `Presencial`.

A segunda revisão (`a7c91d2e4f60`) adiciona a coluna `modalidade` à tabela `turma`.
O valor padrão da migração preenche os registros que já existiam, sem apagar os dados.

## Aplicar no banco local

1. Configure a variável `DATABASE_URL` no arquivo `.env` (não compartilhe esse arquivo).
2. Ative o ambiente virtual e instale as dependências:
   `pip install -r requirements.txt`
3. Na raiz do projeto, execute:
   `python -m alembic current`
   O banco deve estar na revisão `309f587ecc01`.
4. Aplique a nova revisão:
   `python -m alembic upgrade head`
5. Confira a versão:
   `python -m alembic current`
   O resultado esperado é `a7c91d2e4f60`.
6. Para conferir o histórico:
   `python -m alembic history`

Não execute `alembic downgrade` no banco que contém os dados que deseja preservar.
Não exclua nem recrie o banco para aplicar esta evolução.

## Como conferir os dados

Consulte a tabela `turma` no PostgreSQL. A coluna `modalidade` deverá existir.
Turmas cadastradas antes da migração deverão apresentar `Presencial`.
Novas turmas também usarão `Presencial` caso o campo não seja informado.
