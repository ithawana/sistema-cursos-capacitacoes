# Sistema de Cursos e Capacitações

## 1. Sobre o projeto

O **Sistema de Cursos e Capacitações** é uma aplicação desenvolvida em Python para gerenciar cursos de curta e média duração, turmas, instrutores, alunos, matrículas, aulas, avaliações, frequências e resultados.

O sistema permite acompanhar a participação e o desempenho dos alunos durante as capacitações, calcular seus progressos e determinar a situação de conclusão de cada matrícula, considerando os critérios definidos para cada turma.

A aplicação foi desenvolvida como parte do Trabalho Prático 2 da disciplina **QXD0099 – Desenvolvimento de Software para Persistência**, da Universidade Federal do Ceará (UFC), Campus Quixadá.

### Objetivos principais

- Gerenciar cursos, turmas, instrutores e alunos.
- Realizar matrículas de alunos em diferentes turmas.
- Registrar aulas, frequências e avaliações.
- Acompanhar o desempenho individual dos participantes.
- Identificar alunos aprovados, reprovados, abandonados ou com matrículas em andamento.
- Consultar o histórico de capacitações dos alunos.
- Emitir certificados para matrículas que atendam aos critérios estabelecidos.
- Gerar estatísticas para auxiliar o acompanhamento das capacitações.

## 2. Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem de programação |
| FastAPI | Desenvolvimento da API REST |
| SQLModel | Mapeamento objeto-relacional e validação dos dados |
| SQLAlchemy | Comunicação com o banco de dados |
| PostgreSQL | Banco de dados principal |
| SQLite | Banco alternativo para execução local |
| Alembic | Controle de versões e migrações do banco |
| Pydantic | Validação dos dados recebidos |
| Uvicorn | Servidor para execução da API |
| python-dotenv | Carregamento das variáveis de ambiente |

## 3. Organização do projeto

A estrutura de diretórios está organizada da seguinte maneira:

```text
sistema-cursos-capacitacoes/
│
├── alembic/
│   └── versions/
│       ├── 309f587ecc01_criacao_inicial_das_tabelas.py
│       └── 1f01ee2ca462_adicao_do_atributo_modalidade_na_.py
│
├── app/
│   ├── crud/
│   │   ├── aluno.py
│   │   ├── aula.py
│   │   ├── avaliacao.py
│   │   ├── consultas.py
│   │   ├── curso.py
│   │   ├── instrutor.py
│   │   ├── matricula.py
│   │   └── turma.py
│   │
│   ├── models/
│   │   ├── aluno.py
│   │   ├── aula.py
│   │   ├── avaliacao.py
│   │   ├── certificado.py
│   │   ├── curso.py
│   │   ├── instrutor.py
│   │   ├── matricula.py
│   │   ├── matricula_aula.py
│   │   ├── resultado.py
│   │   └── turma.py
│   │
│   ├── routers/
│   │   ├── alunos.py
│   │   ├── aulas.py
│   │   ├── avaliacoes.py
│   │   ├── consultas.py
│   │   ├── cursos.py
│   │   ├── frequencias.py
│   │   ├── instrutores.py
│   │   ├── matriculas.py
│   │   ├── resultados.py
│   │   └── turmas.py
│   │
│   ├── schemas/
│   │   ├── consultas.py
│   │   └── paginacao.py
│   │
│   ├── services/
│   │   ├── certificado.py
│   │   ├── conclusao.py
│   │   ├── frequencia.py
│   │   └── resultado.py
│   │
│   ├── database.py
│   └── main.py
│
├── scripts/
│   └── povoamento.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── README.md
└── requirements.txt
```

### Responsabilidade de cada diretório

- **app/models:** define as entidades, seus atributos, chaves primárias, chaves estrangeiras e relacionamentos.
- **app/crud:** concentra as operações de criação, consulta, atualização e exclusão dos registros.
- **app/routers:** disponibiliza os endpoints da API e recebe as requisições HTTP.
- **app/services:** implementa funcionalidades específicas e regras de negócio, como frequência, resultados, conclusão e emissão de certificados.
- **app/schemas:** define estruturas de dados utilizadas nas consultas e respostas específicas.
- **app/database.py:** configura a conexão com o banco e disponibiliza as sessões.
- **scripts:** contém scripts auxiliares, incluindo o povoamento inicial do banco.
- **alembic:** armazena as configurações e versões das migrações do banco de dados.

## 4. Modelo de dados

O sistema possui dez entidades principais:

| Entidade | Descrição |
|---|---|
| Aluno | Armazena os dados pessoais dos participantes. |
| Instrutor | Armazena os dados dos profissionais responsáveis pelas turmas. |
| Curso | Contém nome, objetivos, conteúdo programático e carga horária. |
| Turma | Representa uma oferta de determinado curso, com datas, vagas, modalidade e critérios de conclusão. |
| Matrícula | Relaciona um aluno a uma turma e registra sua situação. |
| Aula | Armazena as aulas realizadas em cada turma. |
| Avaliação | Define as avaliações aplicadas em cada turma. |
| Matrícula_Aula | Relaciona matrículas e aulas, registrando a frequência. |
| ResultadoAvaliacao | Registra as notas dos alunos em cada avaliação. |
| Certificado | Armazena os certificados emitidos para as matrículas. |

### Principais relacionamentos

- Um curso pode possuir várias turmas (1:N).
- Um instrutor pode ser responsável por várias turmas (1:N).
- Uma turma pertence a um curso e possui um instrutor responsável.
- Uma turma pode possuir várias aulas (1:N).
- Uma turma pode possuir várias avaliações (1:N).
- Um aluno pode possuir várias matrículas (1:N).
- Uma turma pode possuir várias matrículas (1:N).
- Alunos e turmas possuem relacionamento N:N, realizado por meio da entidade Matrícula.
- Matrículas e aulas possuem relacionamento N:N, realizado por meio da entidade Matrícula_Aula.
- Matrículas e avaliações possuem relacionamento N:N, realizado por meio da entidade ResultadoAvaliacao.
- Uma matrícula pode possuir um certificado (1:1).

### Restrições de integridade

O sistema utiliza chaves primárias, chaves estrangeiras, campos obrigatórios e restrições de unicidade.

Entre as principais regras:

- CPF e e-mail de alunos devem ser únicos.
- CPF e e-mail de instrutores devem ser únicos.
- O nome do curso deve ser único.
- Um aluno não pode possuir duas matrículas na mesma turma.
- Uma matrícula não pode registrar duas frequências para a mesma aula.
- Uma matrícula não pode possuir dois resultados para a mesma avaliação.
- Um certificado está associado a uma única matrícula.
- O código de validação do certificado deve ser único.

## 5. Requisitos para execução

Antes de iniciar, é necessário possuir:

- Python 3.10 ou superior.
- PostgreSQL instalado e em execução, para utilizar o banco principal.
- Git instalado.
- Um editor de código, como Visual Studio Code.
- Acesso ao repositório do projeto.

## 6. Instalação e configuração do ambiente

### 6.1. Clonar o repositório

Abra o terminal e execute:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd sistema-cursos-capacitacoes
```

Substitua `URL_DO_REPOSITORIO` pelo endereço real do repositório GitHub.

### 6.2. Criar o ambiente virtual

O ambiente virtual permite instalar as dependências do projeto de maneira isolada.

No Windows, execute:

```powershell
py -m venv .venv
```

### 6.3. Ativar o ambiente virtual

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a execução do script, utilize:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois, execute novamente o comando de ativação.

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Quando o ambiente estiver ativado, o terminal apresentará o nome `.venv` antes do caminho atual.

### 6.4. Instalar as dependências

Com o ambiente virtual ativado, execute:

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém as bibliotecas necessárias para executar o sistema.

## 7. Configuração do banco de dados

O projeto utiliza a variável de ambiente `DATABASE_URL` para definir qual banco de dados será utilizado.

A configuração é carregada pelo arquivo `app/database.py` por meio da biblioteca `python-dotenv`.

### 7.1. Criar o banco PostgreSQL

Primeiramente, abra o PostgreSQL utilizando o pgAdmin ou o terminal e crie um banco de dados com o nome:

```sql
CREATE DATABASE sistema_curso;
```

Cada integrante deverá possuir seu próprio banco de dados local.

### 7.2. Configurar o arquivo .env

Na raiz do projeto, copie o arquivo `.env.example` e crie um novo arquivo chamado `.env`.

O conteúdo deverá seguir este formato:

```env
DATABASE_URL=postgresql+psycopg2://postgres:SUA_SENHA@localhost:5432/sistema_curso
```

Substitua:

- `postgres`: pelo usuário do PostgreSQL.
- `SUA_SENHA`: pela senha configurada no PostgreSQL.
- `localhost`: pelo endereço do servidor.
- `5432`: pela porta utilizada pelo PostgreSQL.
- `sistema_curso`: pelo nome do banco criado.

**Importante:** o arquivo `.env` contém informações de conexão e não deve ser enviado ao GitHub. Cada integrante deve configurar seu próprio arquivo localmente.

O arquivo `.env.example` serve apenas como modelo de configuração.

### 7.3. Utilizar SQLite (alternativa)

O projeto também permite configurar a conexão com SQLite.

Para isso, altere a variável `DATABASE_URL` no arquivo `.env`:

```env
DATABASE_URL=sqlite:///./database.db
```

O arquivo `database.db` será utilizado como banco SQLite no diretório do projeto.

Para retornar ao PostgreSQL, basta restaurar a configuração anterior.

A alteração da conexão é realizada por variável de ambiente, sem necessidade de modificar os modelos, routers ou operações CRUD.

## 8. Configuração e execução das migrações com Alembic

O projeto utiliza Alembic para controlar a evolução da estrutura do banco de dados.

As migrações permitem criar e modificar tabelas e colunas sem precisar excluir e recriar manualmente o banco.

### 8.1. Estrutura inicial das migrações

O projeto possui duas versões:

**Primeira migração — `309f587ecc01`**

Responsável pela criação inicial das dez tabelas do sistema e suas respectivas chaves primárias, chaves estrangeiras e restrições de integridade.

**Segunda migração — `1f01ee2ca462`**

Responsável por adicionar o atributo `modalidade` à entidade Turma.

O atributo possui as seguintes características:

- Tipo: texto.
- Limite: 20 caracteres.
- Obrigatório.
- Valor padrão: `Presencial`.

A migração utiliza um valor padrão no banco para preencher os registros que já existiam antes da inclusão da coluna.

### 8.2. Aplicar as migrações no banco local

Depois de configurar o `.env`, certifique-se de estar na raiz do projeto e execute:

```bash
python -m alembic current
```

Esse comando consulta a versão de migração atualmente aplicada no banco.

Para aplicar todas as migrações pendentes, execute:

```bash
python -m alembic upgrade head
```

O comando aplica as versões necessárias até alcançar a revisão mais recente.

Para conferir novamente a versão:

```bash
python -m alembic current
```

A versão final esperada é:

```text
1f01ee2ca462
```

Para consultar o histórico de migrações:

```bash
python -m alembic history
```

### 8.3. Quando houver alterações futuras no modelo de dados

Sempre que um integrante modificar a estrutura de uma entidade, como adicionar uma coluna, criar uma tabela ou modificar uma chave estrangeira, a alteração deverá ser registrada por meio de uma nova migração.

Para gerar uma migração automaticamente, execute:

```bash
python -m alembic revision --autogenerate -m "descricao_da_alteracao"
```

O arquivo será criado dentro de:

```text
alembic/versions/
```

Antes de aplicar a migração, é necessário abrir o arquivo gerado e conferir se as operações estão corretas.

Depois, aplique a alteração:

```bash
python -m alembic upgrade head
```

**Importante:** todos os integrantes devem receber os arquivos das novas migrações pelo Git e executar `python -m alembic upgrade head` em seus próprios bancos locais.

Não é necessário apagar as tabelas ou criar um banco novo para cada alteração estrutural.

Não execute `downgrade` sem compreender as consequências para os dados existentes.

## 9. Povoamento inicial do banco

O projeto possui um script responsável por inserir dados iniciais para permitir a execução e demonstração das funcionalidades.

O arquivo está localizado em:

```text
scripts/povoamento.py
```

### 9.1. Executar o povoamento

Depois de aplicar as migrações, execute:

```bash
python -m scripts.povoamento
```

O script utiliza as operações CRUD e os serviços existentes para cadastrar os registros e respeitar os relacionamentos entre as entidades.

### 9.2. Dados inseridos

O povoamento cria os seguintes registros:

| Entidade | Quantidade |
|---|---:|
| Alunos | 12 |
| Instrutores | 2 |
| Cursos | 2 |
| Turmas | 3 |
| Matrículas | 16 |
| Aulas | 10 |
| Avaliações | 5 |

Também são registrados dados de frequência e resultados de avaliações.

O script contempla diferentes situações de matrícula, incluindo cancelamento, abandono e finalização conforme os critérios estabelecidos.

### 9.3. Atenção ao executar novamente

O script possui uma verificação inicial que identifica se alguma das principais tabelas já possui registros.

Caso encontre registros, a execução é interrompida com a mensagem:

```text
O banco já possui registros. Utilize um banco vazio.
```

Isso evita duplicidades, mas significa que o script não completa automaticamente um povoamento parcial.

Portanto, execute o povoamento somente uma vez em cada banco recém-configurado e não o execute novamente sem verificar os dados existentes.

O resultado esperado após a execução bem-sucedida é:

```text
Banco povoado com sucesso!
```

## 10. Executar a aplicação

Com o ambiente virtual ativado, as dependências instaladas, o banco configurado e as migrações aplicadas, execute:

```bash
uvicorn app.main:app --reload
```

O parâmetro `--reload` permite reiniciar automaticamente o servidor quando os arquivos do projeto forem modificados.

Quando o servidor estiver funcionando, a API estará disponível em:

```text
http://127.0.0.1:8000
```

### 10.1. Documentação interativa

O FastAPI disponibiliza uma interface Swagger para visualizar e testar os endpoints.

Acesse:

```text
http://127.0.0.1:8000/docs
```

Por meio dessa interface, é possível:

- Visualizar os endpoints disponíveis.
- Consultar os parâmetros necessários.
- Enviar requisições HTTP.
- Cadastrar e consultar registros.
- Atualizar e cancelar registros.
- Visualizar as respostas da API e os códigos HTTP.

Para encerrar a aplicação, pressione `Ctrl + C` no terminal.

## 11. Principais endpoints da API

Os endpoints estão organizados por routers, separados conforme as responsabilidades de cada entidade.

### 11.1. Alunos

Prefixo: `/alunos`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/alunos/` | Cadastrar aluno |
| GET | `/alunos/` | Listar alunos |
| GET | `/alunos/{aluno_id}` | Consultar aluno |
| PATCH | `/alunos/{aluno_id}` | Atualizar aluno |
| DELETE | `/alunos/{aluno_id}` | Excluir aluno |

A listagem permite paginação e filtro pelo nome.

Exemplo:

```text
GET /alunos/?page=1&size=10&nome=Ana
```

### 11.2. Instrutores

Prefixo: `/instrutores`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/instrutores/` | Cadastrar instrutor |
| GET | `/instrutores/` | Listar instrutores |
| GET | `/instrutores/{instrutor_id}` | Consultar instrutor |
| PATCH | `/instrutores/{instrutor_id}` | Atualizar instrutor |
| DELETE | `/instrutores/{instrutor_id}` | Excluir instrutor |

### 11.3. Cursos

Prefixo: `/cursos`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/cursos/` | Cadastrar curso |
| GET | `/cursos/` | Listar cursos |
| GET | `/cursos/{curso_id}` | Consultar curso |
| PATCH | `/cursos/{curso_id}` | Atualizar curso |
| DELETE | `/cursos/{curso_id}` | Excluir curso |

### 11.4. Turmas

Prefixo: `/turmas`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/turmas/` | Cadastrar turma |
| GET | `/turmas/` | Listar turmas |
| GET | `/turmas/{turma_id}` | Consultar turma |
| PATCH | `/turmas/{turma_id}` | Atualizar turma |
| DELETE | `/turmas/{turma_id}` | Excluir turma |

O cadastro e a atualização de turmas consideram informações como curso, instrutor, número de vagas, datas, frequência mínima, nota mínima e modalidade.

### 11.5. Matrículas

Prefixo: `/matriculas`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/matriculas/` | Criar matrícula |
| GET | `/matriculas/` | Listar matrículas |
| GET | `/matriculas/{matricula_id}` | Consultar matrícula |
| PATCH | `/matriculas/{matricula_id}` | Atualizar matrícula |
| DELETE | `/matriculas/{matricula_id}` | Cancelar matrícula |
| GET | `/matriculas/{matricula_id}/progresso` | Consultar progresso |
| PATCH | `/matriculas/{matricula_id}/finalizar` | Finalizar matrícula |
| POST | `/matriculas/{matricula_id}/certificado` | Emitir certificado |
| GET | `/matriculas/{matricula_id}/certificado` | Consultar certificado |

A listagem permite filtrar as matrículas pelo identificador da turma.

Exemplo:

```text
GET /matriculas/?turma_id=1
```

### 11.6. Aulas

Prefixo: `/aulas`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/aulas/` | Cadastrar aula |
| GET | `/aulas/` | Listar aulas |
| GET | `/aulas/{aula_id}` | Consultar aula |
| PATCH | `/aulas/{aula_id}` | Atualizar aula |
| DELETE | `/aulas/{aula_id}` | Excluir aula |

A listagem permite filtrar aulas por turma.

### 11.7. Avaliações

Prefixo: `/avaliacoes`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/avaliacoes/` | Cadastrar avaliação |
| GET | `/avaliacoes/` | Listar avaliações |
| GET | `/avaliacoes/{avaliacao_id}` | Consultar avaliação |
| PATCH | `/avaliacoes/{avaliacao_id}` | Atualizar avaliação |
| DELETE | `/avaliacoes/{avaliacao_id}` | Excluir avaliação |

A listagem permite filtrar avaliações por turma.

### 11.8. Frequências

Prefixo: `/frequencias`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/frequencias/` | Registrar frequência de uma matrícula em uma aula |

A frequência pode ser registrada como `PRESENTE` ou `AUSENTE`.

### 11.9. Resultados das avaliações

Prefixo: `/resultados-avaliacao`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/resultados-avaliacao/` | Registrar resultado de avaliação |

O resultado relaciona uma matrícula a uma avaliação e armazena a nota obtida.

## 12. Consultas específicas do domínio

O sistema possui um conjunto de consultas que utilizam relacionamentos entre as entidades para recuperar informações mais elaboradas.

Prefixo: `/consultas`

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/consultas/turmas/{turma_id}/participantes` | Consultar participantes de uma turma |
| GET | `/consultas/alunos/{aluno_id}/historico` | Consultar histórico de capacitações de um aluno |
| GET | `/consultas/matriculas/situacao` | Consultar matrículas por situação |
| GET | `/consultas/cursos/mais-concluintes` | Identificar cursos com maior quantidade de concluintes |
| GET | `/consultas/turmas/{turma_id}/frequencia` | Consultar frequência dos alunos de uma turma |
| GET | `/consultas/estatisticas` | Consultar estatísticas gerais |

### 12.1. Filtros disponíveis

**Participantes de uma turma:**

```text
GET /consultas/turmas/1/participantes?status=ATIVA
```

Permite filtrar os participantes conforme a situação da matrícula.

**Matrículas por situação:**

```text
GET /consultas/matriculas/situacao?status=APROVADA&curso_id=1
```

Também permite utilizar `turma_id` para restringir os resultados.

**Cursos com mais concluintes:**

```text
GET /consultas/cursos/mais-concluintes?limite=5
```

Também permite informar `data_de` e `data_ate` para filtrar o período.

**Frequência dos alunos:**

```text
GET /consultas/turmas/1/frequencia?apenas_abaixo_minimo=true
```

Permite identificar alunos que não atingiram o percentual mínimo de frequência.

## 13. Regras de negócio e funcionalidades específicas

O projeto possui serviços responsáveis por implementar regras que vão além das validações básicas dos dados.

### 13.1. Controle de frequência

O serviço `app/services/frequencia.py` realiza o registro de frequência dos alunos nas aulas.

A frequência é associada à matrícula e à aula, respeitando a restrição que impede registros duplicados para a mesma combinação.

### 13.2. Registro de resultados

O serviço `app/services/resultado.py` registra as notas dos alunos nas avaliações.

O sistema verifica as associações entre matrículas e avaliações e impede resultados duplicados para a mesma combinação.

### 13.3. Cálculo de progresso e conclusão

O serviço `app/services/conclusao.py` é responsável por acompanhar o progresso das matrículas e determinar se os critérios de conclusão foram atendidos.

São considerados os critérios definidos para cada turma, incluindo frequência mínima e nota mínima quando aplicável.

A funcionalidade pode ser acessada por:

```text
GET /matriculas/{matricula_id}/progresso
```

A finalização pode ser solicitada por:

```text
PATCH /matriculas/{matricula_id}/finalizar
```

A matrícula recebe a situação correspondente ao resultado da avaliação dos critérios de conclusão.

### 13.4. Emissão de certificados

O serviço `app/services/certificado.py` controla a emissão e a consulta dos certificados.

A emissão está associada a uma matrícula e utiliza as regras de conclusão do sistema.

### 13.5. Estatísticas

O endpoint:

```text
GET /consultas/estatisticas
```

retorna informações agregadas sobre os dados armazenados, utilizando consultas ao banco de dados.

## 14. Tratamento de erros

A API utiliza códigos HTTP para representar o resultado das operações.

| Código | Significado |
|---|---|
| 200 | Operação realizada com sucesso |
| 201 | Registro criado |
| 204 | Operação concluída sem conteúdo de resposta |
| 400 | Requisição inválida ou regra de negócio não atendida |
| 404 | Recurso não encontrado |
| 409 | Conflito ou violação de integridade |
| 422 | Dados recebidos inválidos |
| 500 | Erro interno inesperado |

O sistema utiliza mecanismos de tratamento de erros para situações como registros inexistentes, duplicidades, violações de integridade e tentativas de exclusão de registros vinculados a outras entidades.

## 15. Fluxo recomendado para novos integrantes

Para que todos os integrantes executem o projeto corretamente em suas máquinas, a sequência recomendada é:

1. Clonar o repositório GitHub.
2. Entrar na pasta do projeto.
3. Criar o ambiente virtual `.venv`.
4. Ativar o ambiente virtual.
5. Instalar as dependências com `pip install -r requirements.txt`.
6. Criar o banco de dados PostgreSQL local.
7. Criar o arquivo `.env` com a variável `DATABASE_URL`.
8. Executar `python -m alembic current` para verificar a versão do banco.
9. Executar `python -m alembic upgrade head` para aplicar as migrações pendentes.
10. Executar `python -m scripts.povoamento` para inserir os dados iniciais, caso o banco esteja vazio.
11. Executar `uvicorn app.main:app --reload` para iniciar a API.
12. Acessar `http://127.0.0.1:8000/docs` para testar as funcionalidades.

### Quando receber atualizações dos demais integrantes

Sempre que houver alterações enviadas ao repositório:

1. Salvar ou realizar commit das alterações locais.
2. Executar `git pull origin main` para receber as atualizações da branch principal, considerando a branch utilizada pela equipe.
3. Atualizar as dependências caso o `requirements.txt` tenha sido modificado.
4. Executar `python -m alembic upgrade head` para aplicar eventuais novas migrações.
5. Reiniciar a aplicação.
6. Testar as funcionalidades atualizadas.

Não é necessário executar novamente o povoamento quando o banco já possuir os dados iniciais.

## 16. Cuidados importantes durante o desenvolvimento

- Não excluir ou recriar o banco para aplicar alterações estruturais.
- Não compartilhar o arquivo `.env` pelo GitHub.
- Sempre aplicar as migrações recebidas dos demais integrantes antes de executar a aplicação quando houver alterações no esquema.
- Não modificar diretamente o banco sem considerar os modelos e as migrações.
- Respeitar as chaves estrangeiras e as restrições de integridade.
- Evitar cadastrar registros duplicados.
- Não executar o povoamento repetidamente em bancos que já possuem dados.
- Manter os CRUDs, routers, models e services organizados em seus respectivos diretórios.
- Testar as operações pelo Swagger antes de considerar uma funcionalidade concluída.

---

## 17. Considerações finais

O Sistema de Cursos e Capacitações foi desenvolvido para centralizar o gerenciamento das atividades de uma organização responsável pela oferta de cursos e treinamentos.

A aplicação utiliza uma arquitetura organizada em camadas, persistência relacional e migrações controladas, permitindo que diferentes integrantes trabalhem em funcionalidades específicas sem comprometer a estrutura geral do sistema.

A utilização de PostgreSQL, SQLModel, FastAPI e Alembic permite manter os dados persistidos, organizar as operações e evoluir o esquema do banco de maneira controlada.

O projeto busca atender às necessidades de gerenciamento das capacitações, oferecendo recursos para acompanhar matrículas, frequência, avaliações, desempenho e conclusão dos alunos.

**Disciplina:** QXD0099 – Desenvolvimento de Software para Persistência  
**Instituição:** Universidade Federal do Ceará – Campus Quixadá  
**Trabalho:** TP2 – Desenvolvimento de Sistema com Persistência Relacional  
**Tema:** Tema 16 – Sistema de Cursos e Capacitações

**Integrantes:** [Inserir nomes dos integrantes da equipe]