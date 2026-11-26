# Sistema de Cursos e Capacitações

API REST para gerenciamento de cursos, turmas e matrículas, com acompanhamento de frequência, desempenho acadêmico e conclusão de capacitações.

**Universidade Federal do Ceará (UFC) — Campus Quixadá**  
**Disciplina:** QXD0099 — Desenvolvimento de Software para Persistência  
**Professor:** Francisco Victor da Silva Pinheiro  
**Trabalho:** TP2 — Desenvolvimento de Sistema com Persistência Relacional  
**Tema 16:** Sistema de Cursos e Capacitações

## 1. Integrantes

- Ithawana de Oliveira Cunha
- Mariana Kessya de Lavor
- Moacir Silva Abreu

## 2. Contexto e objetivo

O projeto atende ao cenário de uma organização que oferece cursos de curta e média duração e necessita centralizar o controle de alunos, instrutores, turmas, aulas e avaliações. A aplicação permite distinguir as características permanentes de um curso das informações específicas de cada oferta, representada pela turma.

A necessidade central do sistema é acompanhar a participação e o desempenho dos alunos, calcular seu progresso e determinar a situação de conclusão de cada matrícula de acordo com os critérios de frequência e nota estabelecidos para a turma.

Entre as funcionalidades desenvolvidas estão:

- Cadastro, consulta, atualização e exclusão ou cancelamento dos registros principais.
- Controle de matrículas, vagas, presenças e notas.
- Cálculo de frequência e desempenho, aprovação e reprovação de alunos.
- Emissão e consulta de certificados vinculados às matrículas aprovadas.
- Paginação, filtros, consultas relacionadas, consultas complexas e estatísticas.
- Persistência relacional, migrações com Alembic e povoamento inicial do banco.

## 3. Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem de programação |
| FastAPI | Desenvolvimento da API REST e documentação OpenAPI/Swagger |
| SQLModel | Definição dos modelos ORM e schemas |
| SQLAlchemy | Engine, operações de persistência, consultas e relacionamentos |
| Pydantic | Validação dos dados de entrada e saída |
| PostgreSQL | Banco de dados relacional principal |
| SQLite | Alternativa de banco configurável |
| Alembic | Versionamento e evolução do esquema relacional |
| psycopg2-binary | Driver de conexão com PostgreSQL |
| Uvicorn | Servidor ASGI para execução da API |
| python-dotenv | Carregamento da variável de ambiente `DATABASE_URL` |

## 4. Organização do projeto

```text
sistema-cursos-capacitacoes/
├── app/
│   ├── crud/               # Operações de persistência e consultas
│   ├── models/             # Entidades ORM e schemas das entidades
│   ├── routers/            # Endpoints da API organizados com APIRouter
│   ├── schemas/            # Estruturas de resposta de consultas e paginação
│   ├── services/           # Frequência, resultados, conclusão e certificado
│   ├── database.py         # Conexão com o banco e sessões
│   └── main.py             # Instância FastAPI e registro dos routers
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/           # Revisões do esquema do banco
├── scripts/
│   └── povoamento.py       # Inserção de dados de demonstração
├── .env.example            # Modelo de configuração local
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

A aplicação separa as responsabilidades entre os routers, que recebem as requisições HTTP, os CRUDs e serviços, que executam as operações e regras de negócio, e os models, que representam os dados persistidos. Os schemas `Create`, `Public` e `Update` das entidades são definidos nos respectivos arquivos de models, conforme o padrão do SQLModel utilizado no projeto.

O arquivo `database.py` configura a `engine` a partir da variável `DATABASE_URL`. A dependência `getSession()` disponibiliza uma sessão para as operações da API e encerra a sessão ao finalizar seu uso.

## 5. Modelo de dados

O sistema possui dez tabelas de domínio, sendo sete entidades principais com operações CRUD e três entidades destinadas ao registro de frequência, resultados e certificados.

| Entidade | Responsabilidade |
|---|---|
| Aluno | Dados dos participantes das capacitações |
| Instrutor | Dados dos responsáveis pelas turmas |
| Curso | Nome, objetivos, conteúdo programático e carga horária prevista |
| Turma | Oferta específica de um curso, com instrutor, vagas, período, modalidade e critérios de aprovação |
| Matrícula | Inscrição de um aluno em uma turma e sua situação acadêmica |
| Aula | Data, horário, duração em minutos e conteúdo de uma aula |
| Avaliação | Atividade avaliativa da turma, com nota máxima e peso |
| Matrícula_Aula | Registro de presença ou ausência de uma matrícula em uma aula |
| ResultadoAvaliacao | Nota e comentário associados a uma matrícula e uma avaliação |
| Certificado | Registro de emissão para uma matrícula aprovada |

### 5.1. Relacionamentos entre as entidades

- **1:1 (opcional):** uma matrícula pode possuir no máximo um certificado, e cada certificado pertence a uma única matrícula.
- **1:N:** um curso possui várias turmas; um instrutor pode ministrar várias turmas; uma turma possui várias aulas, avaliações e matrículas; um aluno pode possuir várias matrículas.
- **N:N:** Aluno e Turma são associados por Matrícula; Matrícula e Aula, por Matrícula_Aula; Matrícula e Avaliação, por ResultadoAvaliacao.

O aluno pode participar de diferentes turmas de um mesmo curso, pois a unicidade da matrícula considera o aluno e a turma, não o curso.

### 5.2. Modelo relacional

Os nomes abaixo correspondem às tabelas do banco. **PK** indica chave primária, **FK** indica chave estrangeira e **UQ** indica restrição de unicidade.

| Tabela | PK | FK | Demais atributos |
|---|---|---|---|
| `aluno` | `id` | — | `nome`, `cpf` (UQ), `email` (UQ), `data_nascimento` |
| `instrutor` | `id` | — | `nome`, `cpf` (UQ), `email` (UQ), `data_nascimento` |
| `curso` | `id` | — | `nome` (UQ), `objetivos`, `conteudo_programatico`, `carga_horaria` |
| `turma` | `id` | `curso_id → curso.id`, `instrutor_id → instrutor.id` | `numero_vagas`, `data_inicio`, `data_fim`, `frequencia_minima`, `nota_minima`, `modalidade` |
| `matricula` | `id` | `aluno_id → aluno.id`, `turma_id → turma.id` | `status`, `data_matricula`, `data_cancelamento` |
| `aula` | `id` | `turma_id → turma.id` | `data`, `horario`, `duracao`, `conteudo` |
| `avaliacao` | `id` | `turma_id → turma.id` | `titulo`, `data`, `nota_maxima`, `peso` |
| `matricula_aula` | `id` | `matricula_id → matricula.id`, `aula_id → aula.id` | `frequencia`, `data_aula` |
| `resultadoavaliacao` | `id` | `matricula_id → matricula.id`, `avaliacao_id → avaliacao.id` | `nota`, `comentario` |
| `certificado` | `id` | `matricula_id → matricula.id` (UQ) | `data_emissao`, `codigo_validacao` (UQ) |

Restrições de unicidade compostas:

- `matricula`: (`aluno_id`, `turma_id`).
- `matricula_aula`: (`matricula_id`, `aula_id`).
- `resultadoavaliacao`: (`matricula_id`, `avaliacao_id`).

Os models também definem campos obrigatórios e validações de valores, como carga horária de 1 a 200 horas, duração positiva de aulas, frequência mínima de 0 a 100, notas de 0 a 10 e peso positivo de avaliações. As validações de entrada são complementadas pelas regras de negócio nos CRUDs e serviços.

O Alembic mantém ainda a tabela auxiliar `alembic_version`, que não é uma entidade do domínio.

## 6. Instalação e configuração do ambiente

### 6.1. Pré-requisitos

- Python 3.10 ou superior.
- Git, caso a instalação seja feita por clonagem.
- PostgreSQL instalado e em execução para utilizar o banco principal.
- pgAdmin (opcional), para visualizar e administrar o PostgreSQL.

### 6.2. Obter o projeto

Clone o repositório ou extraia o ZIP do projeto e abra a pasta que contém `requirements.txt` e `alembic.ini`.

<!-- PREENCHER: substituir URL_DO_REPOSITORIO pela URL real do GitHub antes da entrega. -->

```bash
git clone URL_DO_REPOSITORIO
cd sistema-cursos-capacitacoes
```

### 6.3. Criar e ativar o ambiente virtual

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear o script de ativação, permita sua execução na sessão atual com `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` e repita a ativação.

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 6.4. Instalar as dependências

Com o ambiente virtual ativado, execute:

```bash
python -m pip install -r requirements.txt
```

## 7. Configuração do banco de dados

### 7.1. PostgreSQL — banco principal

Crie um banco local chamado `sistema_curso`, utilizando o pgAdmin ou o terminal do PostgreSQL. Se optar pelo SQL, execute o comando conectado a um banco existente, como `postgres`:

```sql
CREATE DATABASE sistema_curso;
```

Na raiz do projeto, copie `.env.example` para `.env`.

**Windows:**

```powershell
Copy-Item .env.example .env
```

**Linux/macOS:**

```bash
cp .env.example .env
```

Edite o arquivo `.env` com as credenciais locais:

```dotenv
DATABASE_URL=postgresql+psycopg2://postgres:SUA_SENHA@localhost:5432/sistema_curso
```

Substitua `SUA_SENHA` pela senha do PostgreSQL e ajuste usuário, porta e nome do banco, se necessário. Caracteres especiais da senha que interferem na URL devem ser codificados adequadamente.

**Não envie o arquivo `.env` ao GitHub.** Cada integrante utiliza suas próprias credenciais de conexão. O arquivo `.env.example` é apenas um modelo.

### 7.2. SQLite — banco alternativo

A aplicação permite trocar o banco por meio da variável `DATABASE_URL`, sem alterar models, routers ou CRUDs.

Para utilizar SQLite, interrompa o servidor e substitua temporariamente o conteúdo do `.env` por:

```dotenv
DATABASE_URL=sqlite:///./database.db
```

Aplique as migrações nesse banco, execute o povoamento se o banco estiver vazio e inicie a API seguindo as seções 8 a 10. Para retornar ao PostgreSQL, restaure a URL anterior e reinicie a aplicação.

Os dois bancos são independentes: a troca da conexão não transfere automaticamente os dados de um banco para o outro.

## 8. Migrações com Alembic

O projeto possui duas revisões concluídas, que registram a criação inicial e a evolução do esquema do banco de dados.

| Revisão | Alteração realizada |
|---|---|
| `309f587ecc01` | Criação inicial das dez tabelas de domínio, chaves e restrições |
| `1f01ee2ca462` | Inclusão do atributo `modalidade` na tabela `turma` |

A segunda revisão adiciona uma coluna de texto com limite de 20 caracteres, obrigatória e com valor padrão `Presencial`. O valor padrão definido no banco permite preencher os registros existentes sem excluir ou recriar a tabela.

```text
<base> → 309f587ecc01 → 1f01ee2ca462 (head)
```

### 8.1. Aplicar as revisões em uma nova instalação

Depois de configurar o banco, execute na raiz do projeto:

```bash
python -m alembic upgrade head
```

Esse comando aplica somente as revisões ainda não executadas no banco escolhido. Não é necessário gerar uma nova revisão, pois os arquivos das duas migrações já estão incluídos no repositório.

### 8.2. Consultar a versão e o histórico

```bash
python -m alembic current
python -m alembic history
```

A versão atual esperada após a aplicação das duas migrações é:

```text
1f01ee2ca462 (head)
```

A evolução da primeira para a segunda revisão foi executada com sucesso no PostgreSQL local durante o desenvolvimento. O comando `current` confirmou a revisão `1f01ee2ca462 (head)`.

A versão também pode ser consultada pelo Query Tool do pgAdmin:

```sql
SELECT * FROM public.alembic_version;
```

As migrações estão prontas e versionadas. Os comandos desta seção servem para preparar novos ambientes ou demonstrar o funcionamento do Alembic, não representam uma etapa de implementação pendente.

## 9. Povoamento inicial

O arquivo `scripts/povoamento.py` prepara os dados de demonstração do sistema, reutilizando os CRUDs e os serviços existentes para respeitar as regras de negócio e os relacionamentos.

Com as migrações aplicadas e o banco sem registros de domínio, execute:

```bash
python -m scripts.povoamento
```

Saída de sucesso:

```text
Banco povoado com sucesso!
```

### 9.1. Dados gerados

| Entidade | Quantidade prevista em um povoamento completo |
|---|---:|
| Alunos | 12 |
| Instrutores | 2 |
| Cursos | 2 |
| Turmas | 3 |
| Matrículas | 16 |
| Aulas | 10 |
| Avaliações | 5 |
| Registros de frequência | 52 |
| Resultados de avaliações | 26 |
| Certificados | 5 |

Os dados são fictícios. As datas são calculadas a partir do dia de execução do script, permitindo criar duas turmas encerradas e uma turma em andamento.

A distribuição prevista das matrículas é de cinco aprovadas, cinco reprovadas, quatro ativas, uma cancelada e uma abandonada. A conclusão das turmas encerradas é calculada pelo próprio serviço de conclusão, e os certificados são emitidos automaticamente para as matrículas aprovadas.

Essa distribuição permite demonstrar a paginação, os filtros, as cardinalidades 1:1, 1:N e N:N, os relatórios de frequência, as consultas de histórico e as estatísticas. As quantidades acima são as previstas pelo código em um banco vazio, antes de cadastros ou alterações realizados em testes.

### 9.2. Reexecução do script

O povoamento foi executado com sucesso no PostgreSQL local durante o desenvolvimento. Em um banco já povoado, não é necessário executá-lo novamente.

O script verifica a existência de registros e interrompe a execução quando encontra dados nas tabelas verificadas, evitando a duplicação dos cadastros. Como as operações de cadastro persistem os registros ao longo do processo, uma execução interrompida pode deixar dados parciais; o script não completa automaticamente esse povoamento. Para uma nova demonstração, utilize preferencialmente outro banco vazio, sem apagar os dados existentes.

## 10. Execução da aplicação

Na raiz do projeto, com o ambiente virtual ativado e o banco configurado, execute:

```bash
python -m uvicorn app.main:app --reload
```

A API fica disponível localmente em `http://127.0.0.1:8000`.

- [Swagger UI — documentação e testes dos endpoints](http://127.0.0.1:8000/docs)
- [Especificação OpenAPI](http://127.0.0.1:8000/openapi.json)

No Swagger, selecione um endpoint, clique em **Try it out**, informe os parâmetros ou o corpo JSON e clique em **Execute**. Para encerrar o servidor, pressione `Ctrl + C` no terminal.

## 11. Principais endpoints

### 11.1. Operações CRUD das entidades principais

| Recurso | Cadastro e listagem | Consulta, atualização e exclusão |
|---|---|---|
| Aluno | `POST /alunos/` · `GET /alunos/` | `GET`, `PATCH`, `DELETE /alunos/{aluno_id}` |
| Instrutor | `POST /instrutores/` · `GET /instrutores/` | `GET`, `PATCH`, `DELETE /instrutores/{instrutor_id}` |
| Curso | `POST /cursos/` · `GET /cursos/` | `GET`, `PATCH`, `DELETE /cursos/{curso_id}` |
| Turma | `POST /turmas/` · `GET /turmas/` | `GET`, `PATCH`, `DELETE /turmas/{turma_id}` |
| Matrícula | `POST /matriculas/` · `GET /matriculas/` | `GET`, `PATCH`, `DELETE /matriculas/{matricula_id}` |
| Aula | `POST /aulas/` · `GET /aulas/` | `GET`, `PATCH`, `DELETE /aulas/{aula_id}` |
| Avaliação | `POST /avaliacoes/` · `GET /avaliacoes/` | `GET`, `PATCH`, `DELETE /avaliacoes/{avaliacao_id}` |

O método `PATCH` permite a atualização parcial. O `DELETE` de matrícula representa cancelamento lógico, preservando o registro e armazenando a data de cancelamento. As exclusões de outras entidades consideram a existência de registros dependentes.

### 11.2. Operações específicas do domínio

| Método | Endpoint | Finalidade |
|---|---|---|
| POST | `/frequencias/` | Registrar presença ou ausência de um aluno em uma aula |
| POST | `/resultados-avaliacao/` | Registrar a nota de uma matrícula em uma avaliação |
| GET | `/matriculas/{matricula_id}/progresso` | Consultar frequência, desempenho e situação |
| PATCH | `/matriculas/{matricula_id}/finalizar` | Persistir a aprovação ou reprovação calculada |
| POST | `/matriculas/{matricula_id}/certificado` | Emitir certificado para matrícula aprovada |
| GET | `/matriculas/{matricula_id}/certificado` | Consultar certificado emitido |

A emissão gera um registro no banco com data e código único no formato `CERT-{matricula_id}`. Não há geração de arquivos PDF; o certificado é representado como recurso da API.

### 11.3. Exemplo de registro de frequência e nota

**POST `/frequencias/`:**

```json
{
  "matricula_id": 11,
  "aula_id": 9,
  "frequencia": "PRESENTE"
}
```

**POST `/resultados-avaliacao/`:**

```json
{
  "matricula_id": 11,
  "avaliacao_id": 5,
  "nota": 8.5,
  "comentario": "Bom desempenho"
}
```

Os IDs são ilustrativos: para executar, escolha uma matrícula ativa e uma aula ou avaliação da mesma turma, sem registro anterior. O povoamento já pode ter registrado presenças e notas para os IDs de exemplo.

## 12. Paginação e filtros

A listagem de alunos utiliza `offset()` e `limit()` na consulta SQLModel, evitando carregar todos os registros para depois paginar em memória. Os resultados são ordenados pelo identificador do aluno.

| Parâmetro | Comportamento |
|---|---|
| `page` | Página solicitada, iniciando em 1 (padrão: 1) |
| `size` | Quantidade por página, de 1 a 100 (padrão: 10) |
| `nome` | Busca parcial por nome, sem distinguir maiúsculas e minúsculas |

O deslocamento é calculado por `(page - 1) * size`. A resposta contém a lista de alunos da página solicitada.

Exemplos de consultas:

```http
GET /alunos/?page=1&size=5
GET /alunos/?page=2&size=5
GET /alunos/?nome=Ana
GET /matriculas/?turma_id=1
GET /aulas/?turma_id=1
GET /avaliacoes/?turma_id=1
```

O nome do aluno é um critério geral. O vínculo com a turma e a situação da matrícula são critérios específicos do domínio, além dos demais filtros disponíveis nas consultas relacionadas e complexas.

## 13. Consultas específicas, complexas e estatísticas

### 13.1. Consultas envolvendo relacionamentos (F10)

| Endpoint GET | Entidades e finalidade |
|---|---|
| `/consultas/turmas/{turma_id}/participantes` | Matrícula e Aluno: lista os participantes da turma, com filtro opcional por `status` |
| `/consultas/alunos/{aluno_id}/historico` | Matrícula, Turma, Curso e Instrutor: recupera o histórico de capacitações do aluno |
| `/consultas/matriculas/situacao` | Matrícula, Aluno, Turma e Curso: busca por `status` obrigatório e filtros opcionais `curso_id` e `turma_id` |

```http
GET /consultas/turmas/1/participantes?status=APROVADA
GET /consultas/alunos/5/historico
GET /consultas/matriculas/situacao?status=ATIVA&turma_id=3
```

### 13.2. Consultas complexas (F11)

| Endpoint GET | Descrição |
|---|---|
| `/consultas/cursos/mais-concluintes` | Utiliza JOIN, COUNT, GROUP BY, ORDER BY e LIMIT para classificar cursos pela quantidade de matrículas aprovadas. Aceita `limite` (1 a 50, padrão 5), `data_de` e `data_ate`, considerando o término da turma. |
| `/consultas/turmas/{turma_id}/frequencia` | Utiliza LEFT JOIN, COUNT e GROUP BY para calcular a frequência dos participantes, excluindo matrículas canceladas. O parâmetro `apenas_abaixo_minimo=true` utiliza HAVING para identificar alunos abaixo do mínimo exigido. |

```http
GET /consultas/cursos/mais-concluintes?limite=5
GET /consultas/turmas/1/frequencia?apenas_abaixo_minimo=true
```

As consultas utilizam dados persistidos e os relacionamentos reais das tabelas, em vez de resultados simulados ou valores fixos.

### 13.3. Estatísticas e agregações (F12)

**GET `/consultas/estatisticas`**

O endpoint apresenta os totais de alunos, cursos e turmas, as matrículas agrupadas por status e os indicadores de cada curso. São utilizadas funções de agregação como `COUNT`, `AVG` e `GROUP BY`.

A taxa de aprovação considera apenas matrículas concluídas: aprovadas ÷ (aprovadas + reprovadas) × 100. A média de notas por curso corresponde à média dos registros de notas de avaliação, não à média ponderada final individual. Quando não houver dados suficientes, os respectivos indicadores podem retornar `null`.

## 14. Regras de negócio

O projeto implementa as cinco regras principais definidas no planejamento, além de validações complementares de integridade e consistência.

| Regra | Comportamento implementado | Arquivo |
|---|---|---|
| RN01 — Matrícula duplicada | Impede que o mesmo aluno seja matriculado duas vezes na mesma turma | `app/crud/matricula.py` |
| RN02 — Limite de vagas | Conta matrículas ativas e impede novas inscrições quando a capacidade é atingida | `app/crud/matricula.py` |
| RN03 — Frequência | Exige matrícula ativa e aula da mesma turma; impede duplicidade de presença | `app/services/frequencia.py` |
| RN04 — Notas | Exige matrícula ativa e avaliação da mesma turma; impede nota acima do máximo e duplicidade de resultado | `app/services/resultado.py` |
| RN05 — Aprovação e certificado | A aprovação é determinada pelo serviço de conclusão; somente matrícula aprovada pode receber um certificado, limitado a um por matrícula | `app/services/conclusao.py` e `app/services/certificado.py` |

A aplicação também verifica referências inexistentes, validade de períodos, dependências antes de exclusões e impede a alteração manual do status para `APROVADA` ou `REPROVADA` pelo CRUD comum de matrícula.

## 15. Funcionalidade específica — progresso e conclusão (F17)

O serviço `app/services/conclusao.py` utiliza as relações entre Matrícula, Turma, Aula, Matrícula_Aula, Avaliação e ResultadoAvaliacao para acompanhar o desempenho dos alunos.

### 15.1. Frequência

A frequência é calculada pela quantidade de presenças em relação à quantidade de aulas da turma com data até o dia da consulta:

```text
frequencia = (presencas / aulas_realizadas) * 100
```

A frequência é calculada por número de aulas, e não pela soma de suas durações. Se nenhuma aula tiver sido realizada, o percentual retorna `null`.

### 15.2. Desempenho

O sistema considera os resultados das avaliações com data até o dia da consulta. As notas são normalizadas para a escala de 0 a 10 e ponderadas de acordo com o peso de cada avaliação:

```text
nota_normalizada = (nota_obtida * 10) / nota_maxima
nota_final = soma(nota_normalizada * peso) / soma(peso)
```

Se ainda não houver resultados para calcular a média, a nota retorna `null`.

### 15.3. Determinação e persistência da conclusão

A finalização exige matrícula ativa, data de término da turma atingida, ao menos uma aula realizada, registros de frequência para todas as aulas contabilizadas e resultados de todas as avaliações da turma. Se houver nota mínima configurada, deve existir nota calculada.

Uma matrícula apta à finalização recebe a situação `APROVADA` se atingir a frequência mínima e, quando exigida, a nota mínima. Caso contrário, recebe `REPROVADA`. Se ainda não puder finalizar, a situação registrada é mantida. As matrículas canceladas, abandonadas ou inativas não são finalizadas pelo serviço.

| Frequência mínima | Nota mínima | Frequência obtida | Nota obtida | Resultado ao finalizar |
|---:|---:|---:|---:|---|
| 75% | 7,0 | 100% | 8,5 | APROVADA |
| 75% | 7,0 | 0% | 8,5 | REPROVADA |
| 75% | 7,0 | 100% | 5,0 | REPROVADA |

A consulta `GET /matriculas/{matricula_id}/progresso` retorna a frequência, a nota final, os critérios mínimos, a situação calculada e o indicador `pode_finalizar`. A operação `PATCH /matriculas/{matricula_id}/finalizar` grava o status definitivo no banco de dados. O certificado pode ser emitido após a aprovação persistida.

O sistema mantém as matrículas e seus registros de participação, notas e status de conclusão. Na implementação atual, os percentuais, as médias e os critérios exibidos na consulta de progresso são recalculados a partir dos registros e configurações vigentes, não armazenados como uma fotografia imutável do resultado final.

## 16. Tratamento de erros

A API utiliza `HTTPException`, validações dos schemas e tratamento de exceções de integridade para comunicar erros de operação. Nos pontos em que `IntegrityError` é tratado, utiliza-se `rollback()` para desfazer a transação que falhou.

| Código HTTP | Aplicação |
|---|---|
| 200 | Consulta ou atualização bem-sucedida |
| 201 | Registro criado |
| 204 | Exclusão ou cancelamento realizado sem corpo de resposta |
| 400 | Requisição inválida ou regra de negócio não atendida |
| 404 | Registro ou referência não encontrada |
| 409 | Conflito de cadastro, duplicidade, turma lotada ou dependência de registros |
| 422 | Dados inválidos segundo as validações da API |
| 500 | Erro interno inesperado |

Falhas gerais de conexão e outros erros inesperados do banco não possuem tratamento centralizado específico nesta versão. O código 500 não representa um tratamento personalizado para todas essas situações.

## 17. Roteiro de demonstração do trabalho

A apresentação utiliza o banco previamente povoado e a documentação interativa do Swagger. Os IDs dos exemplos devem ser ajustados de acordo com os registros disponíveis no banco local.

| Requisito | Demonstração sugerida |
|---|---|
| F1 a F5 — CRUD | Cadastrar um aluno de teste, listar, consultar por ID, atualizar e excluir; demonstrar o cancelamento de matrícula |
| F6 — Relacionamentos | Apresentar Curso–Turma (1:N), Aluno–Turma via Matrícula (N:N) e Matrícula–Certificado (1:1 opcional) |
| F7 — CRUD Routers | Mostrar os arquivos de `app/routers/` e o registro em `app/main.py` |
| F8 — Paginação | Executar `GET /alunos/` com `page=1`, `size=5`, e depois `page=2` |
| F9 — Filtros | Buscar alunos por nome, matrículas por turma e matrículas por situação |
| F10 — Consultas relacionadas | Executar participantes da turma, histórico do aluno e matrículas por situação |
| F11 — Consultas complexas | Mostrar cursos com mais concluintes e frequência abaixo do mínimo |
| F12 — Estatísticas | Executar `GET /consultas/estatisticas` e explicar as agregações |
| F13 — Regras de negócio | Demonstrar pelo menos três regras, como matrícula duplicada, limite de vagas e nota inválida para a avaliação |
| F14 — Alembic | Mostrar `history`, `current`, os arquivos das duas revisões e o atributo `modalidade` em Turma |
| F15 — PostgreSQL e SQLite | Demonstrar a configuração da conexão e a execução da API com os dois bancos, utilizando os respectivos dados |
| F16 — Povoamento | Mostrar `scripts/povoamento.py` e os registros disponíveis antes de iniciar a demonstração |
| F17 — Funcionalidade específica | Consultar progresso, explicar aprovação/reprovação, finalizar uma matrícula elegível e consultar ou emitir certificado |
| F18 — Erros | Demonstrar respostas 400, 404, 409 e 422, explicando as validações e o tratamento de integridade |

### 17.1. Comprovação da persistência no PostgreSQL

No pgAdmin, selecione o banco `sistema_curso` e abra o Query Tool. As consultas a seguir permitem visualizar os dados já inseridos e a versão de migração registrada:

```sql
SELECT * FROM public.aluno ORDER BY id;
SELECT * FROM public.matricula ORDER BY id;
SELECT * FROM public.certificado ORDER BY id;
SELECT id, modalidade FROM public.turma ORDER BY id;
SELECT * FROM public.alembic_version;
```

Para demonstrar que os dados permanecem persistidos, realize uma operação pelo Swagger, consulte o registro diretamente no PostgreSQL e reinicie a aplicação. O registro deve continuar disponível após a reinicialização.

As migrações e o povoamento já foram executados no PostgreSQL local. A troca para SQLite segue a configuração da seção 7.2; a execução em cada banco deve ser demonstrada no ambiente correspondente.

---

Projeto acadêmico desenvolvido para a disciplina de Desenvolvimento de Software para Persistência — UFC, Campus Quixadá.