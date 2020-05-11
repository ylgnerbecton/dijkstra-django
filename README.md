
# Bexs Challenge

O projeto tem como objetivo apresentar a menor rota de viagem do usuário.

## Solução utilizada
Utilizei a solução de grafo do **algoritmo de Dijkstra**, que soluciona o problema do caminho mais curto num grafo dirigido ou não dirigido com arestas de peso não negativo.

Sendo assim, utilizei para calcular a menor distância entre duas rotas, foi NetworkX uma lib Python para a criação, manipulação, da estrutura e dinâmica e integrado a isso utilizei Injector implementar um padrão de design de injeção de dependência de uma maneira formal.

## Getting Started

``git clone https://github.com/ylgnerbecton/bexs-challenge.git ``

## Pré requisitos
* Python
* Django

## Instalação

python3

``sudo apt-get install python3.6 ``

pip3

-   `sudo apt-get install python3-pip`
-   `pip3 install virtualenv`

django

``pip3 install Django==2.2``

Pasta do projeto

`cd bexs-challenge`

Ambiente virtual python

`python3 -m venv venv`

## Rodando a aplicação

Acesse a pasta raiz do projeto e entre no ambiente

`source venv/bin/activate`

Instale os requirements do projeto

`pip3 install -r requirements.txt`

Rodar projeto

`python3 run.py runserver`

Rodar projeto pelo console

 `routes-file.csv`: argumento do comando
 
`python3 manage.py console routes-file.csv`

![console](https://github.com/ylgnerbecton/bexs-challenge/blob/master/doc/console.png?raw=true)

## Rodando os testes

Comando para testar a aplicação

`` python3 -m unittest discover -s test ``


## Documentação da API

Esta documentação descreve a estrutura da API e exemplos de uso.

### Acesso à API

Acessar endpoit para vizualização pelo Swagger e fazer requisições

Link para acessar pelo swagger `http://127.0.0.1:8000/api/`

post para cadastrar novas rotas
![get para buscar a melhor rota](https://github.com/ylgnerbecton/bexs-challenge/blob/master/doc/get.png?raw=true)

get para buscar a melhor rota
![enter image description here](https://github.com/ylgnerbecton/bexs-challenge/blob/master/doc/post.png?raw=true)

### Route

Os endpoints de rotas possuem a seguinte estrutura:

-   `departure`: saída do aeroporto
-   `arrival`: chegada ao aeroporto
-   `price`: preço do voo

###  Cadastrar rota

`http://127.0.0.1:8000/api/route/`

**Método**: POST

**Request**:
```
{
    "departure": "GRU",
    "arrival": "MIA",
    "price": 30
}
```

**Response**:

```
{"rpstConsultar": 'Cadastro realizado com sucesso'}
```

### Visualizar rota 

`http://127.0.0.1:8000/api/route/{departure}/{arrival}/`

**Método**: GET

**Request**:

```
departure = GRU
arrival = CDG
```

**Response**:

```
{
  "rpstConsultar": "best route: GRU - BRC - SCL - ORL - CDG > $40.0"
}
```