# Products Service Application

Este repositório contém um serviço de gerenciamento de produtos, construído em Python e utilizando PostgreSQL como banco de dados.

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes softwares instalados em sua máquina:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Estrutura do Projeto

- **Docker Compose**: Configura dois containers, um para o banco de dados PostgreSQL e outro para a aplicação Python.
- **Dockerfile**: Define o ambiente de execução da aplicação Python.
- **PostgreSQL**: Utilizado como banco de dados, com a versão 17.
- **Python**: A aplicação é construída em Python 3.11.

## Configuração e Início da Aplicação

Siga os passos abaixo para iniciar a aplicação localmente utilizando Docker e Docker Compose:

### 1. Clonar o repositório

Clone o repositório para sua máquina local

### 2. Configurar o ambiente

O arquivo `docker-compose.yml` já vem pré-configurado com variáveis de ambiente e os serviços necessários. O arquivo define dois serviços principais:

- **db**: Contém o banco de dados PostgreSQL.
- **app**: Contém a aplicação Python.

### 3. Build e execução dos containers

Para iniciar os serviços, utilize o comando abaixo:

```bash
docker-compose up
````

Isso irá:

- Fazer build da aplicação Python.
- Criar e inicializar um container PostgreSQL.
- Rodar as migrações do banco de dados com `alembic upgrade head`.
- Inicializar o servidor da aplicação.

### 4. Acessar a aplicação

A aplicação estará acessível em `http://localhost:3000`, que está mapeado para a porta `3000` dentro do container da aplicação.

O banco de dados PostgreSQL estará disponível localmente na porta `5460`.

### 5. Parar os containers

Para parar e remover os containers, use o comando `docker-compose down`.

## Estrutura dos Arquivos Importantes

- **Dockerfile**: Define como a aplicação Python será containerizada.
- **docker-compose.yml**: Orquestra os serviços da aplicação (banco de dados e aplicação Python).
- **/src**: Contém o código-fonte da aplicação Python.
- **/src**: Contém o testes da aplicação Python.
- **requirements.txt**: Lista as dependências Python que serão instaladas no container.

## Variáveis de Ambiente

Aqui estão algumas variáveis importantes configuradas no `docker-compose.yml`:

- **DB (PostgreSQL)**:
  - POSTGRES_USER: Usuário do banco de dados.
  - POSTGRES_PASSWORD: Senha do banco de dados.
  - POSTGRES_DB: Nome do banco de dados.
- **App**:
  - DATABASE_HOST: Host do banco de dados (neste caso, o nome do serviço `db`).
  - DATABASE_PORT: Porta do banco de dados.
  - DATABASE_USER: Usuário do banco de dados.
  - DATABASE_PASSWORD: Senha do banco de dados.
  - DATABASE_NAME: Nome do banco de dados.
  - SERVER_HOST: Host da servidor Python.
  - SERVER_PORT: Porta da servidor Python.
  - ENVIRONMENT: Define o ambiente de execução (ex: `production`).

## Comandos Úteis

### Para executar testes unitários

Execute o comando:
```bash
pytest
```

### Visualizar logs:

Utilize o comando `docker-compose logs -f` para visualizar os logs dos containers em execução.

### Acessar o container da aplicação:

Use o comando `docker exec -it <container_id> /bin/sh` para acessar o shell dentro do container da aplicação. Substitua `<container_id>` pelo ID ou nome do container.
