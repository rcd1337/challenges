# Sistema APIRestf - Escola ALF

# Installation
Inside the folder `/alf`, start the server by running `python manage.py runserver` in your terminal of choice.

# Routes

### `POST /aluno`  
> Adds a new student
### Example request: 
`curl -X POST -H "Content-type: application/json" -d '{ "name":"Fulaninho" }' 'localhost:8000/aluno'`

### `POST /gabarito`  
> This creates both a new Prova entity and a reference answer sheet
### Example request: 
`curl -X POST -H "Content-type: application/json" -d '{
	"data": [{
			"Quanto é 1+1": "2"
		},
		{
			"Quem foi a primeira pessoa a pisar na lua?": "Neil Armstrong"
		}
	],
	"prova": "geografia/2020.1"
}' 'localhost:8000/gabarito'`

### `POST /resposta`
> Adds the student's answers to a particular test (Prova entity)
### Example request:
`curl -X POST -H "Content-type: application/json" -d '{
  "data": [{
			"Quanto é 1+1": "2"
		},
		{
			"Quem foi a primeira pessoa a pisar na lua?": "Neil Armstrong"
		}
	],
  "prova_id":"1",
  "aluno_id":"1"
}' 'localhost:8000/resposta'`

### `GET /aprovados`
> Lists all approved students
### Example request:
`curl "localhost:8000/aprovados"`
# Notes
- Not using CSRF validation was a design choice, given that this is not the point of the project and could cause problems with cookie validation during tests.