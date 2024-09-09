# ADVICEHEALTH teste técnico


Teste técnico realizado para processo seletivo. 


## Sumário

- [Contexto](#contexto)
- [Tecnologias](#tecnologias)
- [Arquitetura](#arquitetura)
- [Configuração e Instalação](#configuração-e-instalação)
	- [Utilizando o Docker compose](#utilizando-o-docker-compose)
	- [Utilizando somente o Docker](#utilizando-somente-o-docker)
	- [Utilizando o SQLite](#utilizando-o-sqlite)
	- [Rodando os teste unitário com Pytest](#rodando-os-teste-unitário-com-pytest)
	- [Rodando localmente](#rodando-localmente)
- [Endpoints](#endpoints)



## Contexto

Descrição do desafio:  
Nork-Town is a weird place. Crows cawk the misty morning while old men squint.  
It’s a small town, so the mayor had a bright idea to limit the number of cars a person may possess.  
One person may have up to 3 vehicles. The vehicle, registered to a person, may have one color, ‘yellow’, ‘blue’ or ‘gray’.  
And one of three models, ‘hatch’, ‘sedan’ or ‘convertible’. Carford car shop want a system where they can add car owners and cars.  
Car owners may not have cars yet, they need to be marked as a sale opportunity. Cars cannot exist in the system without owners.

## Tecnologias

- [Python](https://www.python.org/)
- [Flask-openapi3](https://luolingchun.github.io/flask-openapi3/v3.x/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [SQLAlchemy-Utils](https://sqlalchemy-utils.readthedocs.io/en/latest/index.html)
- [PostgreSQL](https://www.postgresql.org/)
- [Pytest](https://docs.pytest.org/en/stable/contents.html)
- [Docker](https://docs.docker.com/)
- [Docker compose](https://docs.docker.com/compose/)

## Arquitetura

O sistema é composto por por dois containers:
- car-shop-app (api principal)
- db (database)

O container db contem o database PostgreSQL.  
É possivel utilizar o database SQLite, tanto em arquivo local, quanto `in-memory`, esse sendo usado para a execução dos testes unitários. Com isso o container db é opcional. Isso é configuravel por variável de ambiente.


Estrutura de diretório:
```
.
├── README.md
├── carford_car_shop/
|   ├── blueprint/
|   │   ├── __init__.py
|   │   ├── car_bp.py
|   │   └── customer_bp.py
|   ├── models/
|   │   ├── __init__.py
|   │   ├── base.py
|   │   ├── car.py
|   │   ├── connection.py
|   │   ├── customer.py
|   │   └── user.py
|   ├── schemas/
|   |   ├── __init__.py
|   |   ├── car.py
|   |   ├── common.py
|   |   ├── customers.py
|   |   └── user.py
|   ├── tests/
|   |   ├── __init__.py
|   |   ├── conftest.py
|   |   ├── database_helper.py
|   |   ├── test_authentication.py
|   |   ├── test_cars.py
|   |   └── test_customers.py
|   ├── utils/
|   │   ├── __init__.py
|   │   └── jwt_token.py
|   ├── app.py
|   ├── .env
|   ├── init_app.py
|   ├── logger.py
|   ├── Dockerfile
|   └── requirements.txt
└── docker-compose.yml
```


## Configuração e Instalação

O arquivo `env.sample` contem as variáveis necessárias para o sistema.

> [!IMPORTANT]
Criar um arquivo `.env` contendo as variáveis indicadas. As varáveis 'TESTING', e 'DEV', só devem existir se for necessário usar o SQLite.
Caso contrário não incluir elas. Para os teste passamos essa variavel pelo comando.

As variáveis API_PORT e DEBUG são opcionais para o desenvolvimento. No App é sugerido utilizar a porta 5000, mas caso queira trocar, alterar esse valor pela  variável é possível, mas será necessário alterar as portas no Dockerfile e docker-compose para as portas serem expostas corretamente.
A variável Debug é apenas para o desenvolvimento da aplicação Flask. Ele permite que o Flask rode em debug mode, e é realizado o auto reload quando há alteração de código.

### Utilizando o Docker compose
É necessário ter instalado o [Docker](https://docs.docker.com/engine/install/) e o [Docker Compose](https://docs.docker.com/compose/install/) para subir os serviços automaticamente.  

O arquivo `docker-compose.yml` deverá estar na raiz do projeto com a estrutura de diretórios de todos os serviços montada conforme descrito na seção [Arquitetura](#arquitetura). 

Execute o comando para fazer o build das imagens Docker e inicializar os container na ordem necessária.
```
docker compose up -d
```

Depois que subir todos os containers, pode acessar o endereço em seu navegador
```
http://127.0.0.1:5000/
```

### Utilizando somente o Docker

É necessário ter instalado o [Docker](https://docs.docker.com/engine/install/).

Para subir o ambiente sem o docker compose é importante criar uma network para que os serviços possam se conectar entre si.
Para criar uma network do tipo bridge com o nome de `app-network` execute o comando:
```
docker network create -d bridge app-network
```

Caso já tenha criado algum container, tipo o container db, e queira conectar esse container a network app-network, execute o comando:
```
docker network connect app-network db
```

Depois de criada a network, vamos subir um container com o banco postgres. O container terá o nome de 'db', estará conectado a network criada, a senha do postgres e o volume para a persistência dos dados.
execute os comandos:
```
docker pull postgres
docker run --name db --network app-network -e POSTGRES_PASSWORD=postgres -v ./database/postgres:/var/lib/postgresql/data -d postgres
```

Depois de iniciado o container do postgres podemos subir o outro container.  
Para iniciar o serviço primeiro temos que fazer o build da imagem.
Estando no mesmo nível em que o Dockerfile no diretorio carford_car_shop, executar o comando:
```
docker build -t car-shop-app-image .
```
depois de construída a imagem podemos executar o container com o comando:
```
docker run --name car-shop-app -p 5000:5000 --network app-network -d car-shop-app-image
```
Para acessar o sistema use o endereço:
```
http://127.0.0.1:5000/
```

### Utilizando o SQLite

Com o SQLite não há necessidade de um container com o Postgres. Fazero build da imagem como descrito anteriormente.
```
docker build -t car-shop-app-image .
```
O nome da imagem pode variar. Deve usar o mesmo ao criar o container posteriormente. No caso 'car-shop-app-image'.  
Para direcionar ao SQLite é necessário acrescentar a variavel de ambiente `DEV=true` para percistencia em arquivo local (criado dentro do container), ou `TESTING=true` para o SQLite in-memory.  
Para realmente persistir os dados, é aconselhavel rodar localmente, já que containers são efêmeros. Aqui serve apenas para testes simples.

Rode o comando a seguir para iniciar o container conectando ao SQLite
```
docker run --rm -p 5000:5000 --env DEV=true car-shop-app-image
```

### Rodando os teste unitário com Pytest

Os testes podem ser executados dentro do container.
Use o comando a seguir para subir um container apontando para o SQLite in-memory e em seguida executando todos os testes existentes.
A opção '-v' (verbose) irá apresentar os testes executados
```
docker run --rm -it --env TESTING=true car-shop-app-image pytest -v
```


### Rodando localmente

Fazer o download dos arquivos e instalar as dependências. É aconselhavel criar um ambiente virtual para as dependências.  
Depois de instaladas as dependências contidas no arquivo `requirements.txt`, criar o arquivo `.env` com as variáveis necessárias.  
Executar o script `init_app.py`.  
Utilize as variaveis de ambiente para conectar ao database desejado.  
- "TESTING=true" para SQLite in-memory  
- "DEV=true" para SQLite em arquivo local  

ou usando o postgres como database default. Inserir os dados do seu postgres nas variáveis referentes ao postgres. 
```
python init_app.py
```

## Endpoints

Para a documentação dos endpoints, rodar a aplicação e ir para a rota `/docs`:
```
http://127.0.0.1:5000/docs
```

São apresentadas as opção de documentação `swagger`, `redoc` e `rapidoc`.  
Atraves delas é possivel testar e entender as rotas e suas especificações.  

Para inserir alguns dados no database para teste acessar a rota `/seed`. Irá inserir dados de User, Customer e Car para a finalidade de testes manuais.
```
http://127.0.0.1:5000/seed
```

os endpoints existentes são:

- POST /login
- POST /login/register
- GET /customers
- GET /customers?buyers=true
- GET /customers/<id>
- POST /customers
- DELETE /customers/<id>
- GET /cars
- GET /cars/<id>
- POST /cars
- DELETE /cars/<id>
