
# Bexs Challenge

O projeto tem como objetivo apresentar a menor rota de viagem do usuário.

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

## Rodando os testes

Comando para testar a aplicação

`` python3 -m unittest discover -s test ``


## Documentação da API

Esta documentação descreve a estrutura da API e exemplos de uso.

### Acesso à API




### Route

Os endpoints de rotas possuem a seguinte estrutura:

-   `departure`: saída do aeroporto
-   `arrival`: chegada ao aeroporto
-   `price`: preço do voo

###  Cadastrar rota

`http://127.0.0.1:8000/api/route`

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