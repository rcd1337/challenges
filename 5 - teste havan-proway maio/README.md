# Gerenciador de Operações - Muito Dinheiro

Projeto feito em Python(v. 3.8.6), utilizando Django(v. 3.1.5) como framework e com interface em HTML5.

## Instalação:

#### Setup do gerenciador:
Dentro do folder `/muito_dinheiro`, no terminal de sua escolha:

- executar `python manage.py makemigrations` para que o Django gere os arquivos necessários para do database;
- executar `python manage.py migrate` para que os arquivos sejam executados e o database seja criado;
- executar `python manage.py loaddata currencies.json` para que as moedas e suas cotações pré-definidas sejam adicionadas ao database.
- executar `python manage.py runserver` para que o servidor seja iniciado.

Por padrão, o endereço do servidor será `http://127.0.0.1:8000/`.

#### Setup da ferramenta administrativa `/admin`: (opcional)

Para utilizar o recurso `/admin`, é necessário criar uma conta administrativa. 

No folder `/muito_dinheiro`, execute `python manage.py createsuperuser`.

## Recursos:

`/cadastro_cliente`

Permite cadastrar clientes por nome.

`/cadastrar_operacao`

Permite cadastrar uma nova operação, requerindo os seguintes campos:
- nome do cliente via lista (necessário cadastro prévio via `/cadastro_cliente`);
- moeda origem (lista);
- moeda destino (lista);
- valor a ser convertido.

`/relatorios`

Permite gerar um **Relatóio de Operações** listando todas as operações registradas, requerindo os seguintes campos:
- nome do cliente (via lista).
- intervalo de tempo (limitades inicial e final determinados por operações já cadastradas)

Gerado o relatório, este detalha, para o período selecionado:

- Valor total das conversões efetuadas (em reais);
- Valor total das taxas cobradas (em reais);
- Valor total das operações (em reais).

Detalha também, abaixo, cada operação realizada, contendo:

- Data e hora da operação;
- Moeda de origem;
- Valor a ser convertido (em unidade monetária conforme origem);
- Moeda destino;
- Valor após conversão (em unidade monetária conforme destino);
- Taxa cobrada;
- Valor da operação, correspondente ao **valor da conversão** subtraído pela **taxa cobrada** (em unidade monetária conforme destino).

`/admin`

Interface automática fornecida pelo Django. Permite visualizar e gerenciar de maneira fácil o database (CRUD).

Permite também **adicionar** novas moedas ou **alterar** existentes.

## Observações e decisões:

- Interface do desafio feita inteiramente em HTML com o intúito de facilitar e simplificar seu uso nos dispositivos/browsers utilizados para acessar o gerenciador.

- O total de cada operação (conversão, taxa, operação) é sempre expressado na unidade monetária da moeda destino.

- O total geral para o período selecionado é sempre expressado em Reais.

- As cotações são indexadas em dólares dos estados unidos, com cotação cotação do dia **23/05/2021 - 07:30 GMT-3**. Todas as cotações (caso novas moedas sejam adicionadas posteriormente) devem ser indexadas em dólar estadunidense.
