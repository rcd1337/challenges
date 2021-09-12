# EXTENSO

Projeto feito em Python(v. 3.8.6), utilizando Django(v. 3.1.2) como framework.


## Setup:

Tenha certeza que possui Python e [Django](https://docs.djangoproject.com/en/3.2/topics/install/) instalados. (Siga o link para passo a passo da instalação)

Dentro do folder `/certi`, no terminal de sua escolha:

- executar `python manage.py runserver` para que o servidor seja iniciado.

Por padrão, o endereço do servidor será `http://localhost:8000/`.


## Recursos:

`http://localhost:8000/<número>`

Retorna uma resposta JSON com a versão por extenso do número inteiro especificado na rota `/<número>` com chave "extenso".

Exemplos:

>```http://localhost:8000/1```
>
>retorna: ```{"extenso": "um"}```


>```http://localhost:8000/-1042```
>
>returna: ```{"extenso": "menos mil e quarenta e dois"}```

>```http://localhost:8000/94587```
>
>returna: ```{"extenso": "noventa e quatro mil e quinhentos e oitenta e sete"}```