# Gerenciador - Treinamento ProWay

Projeto feito em Python(v. 3.8.6), utilizando Django(v. 3.1.5) como framework e com interface em HTML puro.

## Instalação:

Dentro do folder `/event_manager/manager`, iniciar o servidor executando `python manage.py runserver` no terminal de sua escolha.

Por padrão, o endereço do servidor será `http://127.0.0.1:8000/`.

## Recursos:

`/cadastro`

Permite cadastrar, em ordem:
- quantidade de salas para eventos que serão disponibilizadas; (redirecionando para `/pre_cadastro_sala`)
- nome e capacidade de cada sala; (redirecionando para `/cadastro_sala`)
- nome e capacidade dos 2 espaços para café; (redirecionando para para `/cadastro_cafe`)
- participantes por nome e sobrenome. (quando os cadastros anteriores estiverem satisfatoriamente finalizados)

`/consulta`

Permite consultar o nome do espaço para café e das salas de evento designadas para o participante especificado.

`/consulta_sala`

Permite consultar a lista de participantes cadastrados na sala de evento especificada e visualizar sua lotação.

`/consulta_cafe`

Permite consultar a lista de participantes cadastrados no espaço para café especificado e visualizar sua lotação.

## Observações e decisões:

- Interface do desafio feita inteiramente em HTML com o intúito de facilitar e simplificar seu uso nos dispositivos/browsers utilizados para acessar o gerenciador.

- Seguindo as exatas definições do desafio, a capacidade máxima dos espaços para café é requerimento obrigatório para o cadastro, porém, não é componente definitivo para o número máximo de participantes cadastrados. Assim, assume-se que o controle deve ser feito pela equipe organizacional.

- A quantidade de espaços para café e de intervalos é predefinida no desafio, sem especificar o momento que acontecerão nem seu atrelamento às etapas do evento.
Portanto, para este desafio, assumiu-se que os intervalos acontecerão simultaneamente nos dois locais.