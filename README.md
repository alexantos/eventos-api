# Produtor rural back

Desenvolvido com django 5.2.4 e drf 3.16.0

### Configurando o projeto

Para configurar o projeto primeiramente devemos configurar algumas variáveis de ambiente obrigatórias no .env:

```
# Itens obrigatórios
SECRET_KEY=django-insecure--_-jn1*3(i0ed#+kv&-eca$d%0v!31d6&95esz_%ex67mg)i#@
DEBUG=True
ALLOWED_HOSTS='*'
SYMPLA_TOKEN=
```

Para isso crie o arquivo .env na raiz do projeto e copie essas variáveis ou utilize o .env.exemplo também disposto na
raiz do projeto

### Configurando o ambiente

Cenários possíveis:

- Configuração local;
- Docker;

### Configuração com docker:

Primeiramente necessita do docker instalado corretamente:<br>
https://docs.docker.com/engine/install/ <br>
Vale a pena se atentar ao linux post install para o caso de ser instalado no linux:<br>
https://docs.docker.com/engine/install/linux-postinstall/ <br>
Essa configuração garante que não será utilizado o comando do docker com sudo que pode ocasionar vazamentos de memória e
falhas no setup.

### Configuração .env para o docker:

Ao utilizar o docker o `compose.yml` desse projeto também tem o postgres como imagem previamente configurada.<br>
Para atender as necessidades dessa imagem já deixei uma configuração fixa do .env:

```
# Configuração fixa para o docker
DJANGO_LOGLEVEL=info
DATABASE_ENGINE=postgresql_psycopg2
DATABASE_NAME=dockerdjango
DATABASE_USERNAME=dbuser
DATABASE_PASSWORD=dbpassword
DATABASE_HOST=db
DATABASE_PORT=5432
```

E então podemos rodar:<br>

```commandline
docker build -t django-docker .
```

Ocorrendo tudo certo já podemos rodar o compose e acessar localmente o sistema:

```commandline
docker compose up --build
```

Para migrar os dados:

```commandline
docker compose run django-web python manage.py migrate
```

E podemos rodar novamente o build:

```commandline
docker compose up --build
```

### Configuração do banco de dados

- PostgreSQL

### Configurando o Postgre localmente

Instalação: https://www.postgresql.org/download/

Devemos acessar o postgres e criar o banco de dados (no meu caso chamei o banco de produtor, mas isso é escolha sua):

```shell
sudo -u postgres psql
```

Criar um usuário (exemplo fictício):

```shell
CREATE USER usuario WITH PASSWORD 'usuario';
```

Criar um banco (database):

```shell
CREATE DATABASE evento;
```

Em alguns será necessária uma configuração mais profunda para dar os privilégios do seu usuário para acessar o
banco.<br>
No caso de uma configuração local (lembrar de não fazer isso em produção) podemos transformar nosso usuário em um
superusuário:

```shell
ALTER ROLE usuario SUPERUSER;
```

Esse comando acima vai garantir o acesso do banco corretamente<br>

### Variáveis de ambiente

Para a configuração que utiliza o postgres será necessário a adição dessas variáveis no arquivo .env:

```
# Variáveis para o PostgreSQL
DATABASE_NAME=evento
DATABASE_USERNAME=usuario
DATABASE_PASSWORD=usuario
```

### Configuração local:

Primeiramente é necessário ter o python instalado:<br>
https://www.python.org/<br>
Para esse projeto utilizei o python 3.12.3.

Então é necessário criar uma 'venv' para assim instalar as dependências do projeto:<br>
https://docs.python.org/3/library/venv.html#creating-virtual-environments
<br>
Resumidamente nas dependências/diretório bastar rodar o comando:<br>

```bash
python -m venv .venv
```

Após a configuração da venv podemos executar o comando abaixo para instalar as dependências do projeto:

```bash
pip install -r requirements.txt
```

Fazemos as migrações das tabelas com:

```bash
python manage.py migrate
```

Por fim podemos rodar localmente o projeto com:

```bash
python manage.py runserver
```

### Rotas utilizadas:

CRUD de eventos interno do sistema (api).
```shell
curl -X 'GET' \
  'http://localhost:8000/api/evento/' \
  -H 'accept: application/json'
```

Atualização de dados baseado na api
```shell
curl -X 'GET' \
  'http://localhost:8000/atualiza-eventos-sympla/' \
  -H 'accept: */*'
```