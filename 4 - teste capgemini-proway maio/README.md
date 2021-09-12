# Gerenciador de Anúncios - Divulga Tudo

Projeto feito em Python(v. 3.8.6), utilizando Django(v. 3.1.5) como framework e com interface em HTML puro.

## Instalação:

#### Setup do gerenciador:
Dentro do folder `/divulga_tudo`, no terminal de sua escolha:

- executar `python manage.py makemigrations` para que o Django gere os arquivos necessários para do database;
- executar `python manage.py migrate` para que os arquivos sejam executados e o database seja criado;
- executar `python manage.py runserver` para que o servidor seja iniciado.

Por padrão, o endereço do servidor será `http://127.0.0.1:8000/`.


#### Setup da ferramenta administrativa `/admin`: (opcional)

Para utilizar o recurso `/admin`, é necessário criar uma conta administrativa. 

No folder `/divulga_tudo`, execute `python manage.py createsuperuser`.

## Recursos:

`/cadastrar_anuncio`

Permite cadastrar um novo anúncio, requerindo os seguintes campos:
- nome do anúncio;
- nome do cliente via lista (necessário cadastro prévio via `/cadastro_cliente`);
- data de início e data de término;
- valor investido (por dia).

`/cadastro_cliente`

Permite cadastrar clientes por nome.

`/relatorios`

Permite selecionar o cliente e visualizar seus anúncios.
Após a seleção, permite gerar relatório do anúncio desejado, possibilitando especificar o intervalo de tempo desejado para o anúncio (por padrão, a seleção já define o período em sua totalidade).

`/relatório`

Acessado somente através da opção "Gerar relatório" em `/relatórios`, apresenta o relatório de determinado anúncio, contendo, para o período selecionado:

- Total do investimento;
- Quantidade máxima de visualizações;
- Quantidade máxima de cliques;
- Quantidade máxima de compartilhamentos.

`/admin`

Interface automática fornecida pelo Django. Permite visualizar e gerenciar de maneira fácil o database (CRUD).
