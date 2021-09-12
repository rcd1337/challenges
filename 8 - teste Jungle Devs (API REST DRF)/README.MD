# Stack:

- Python 3.9.7
- Django 3.1.5
- djangorestframework 3.12.2
- psycopg2 2.8.6
- gunicorn

# Setup:

Clone this repository. Once inside `/jungledevs`, execute the following on your terminal of choice:
```
$ py -m venv env
$ source env/Scripts/activate ('env/bin/activate' if using linux)
$ docker-compose up
$ docker-compose exec web python manage.py migrate
$ docker-compose exec web python manage.py createsuperuser
$ docker-compose exec web python manage.py runserver
```


# Routes

The main server url to access it will be: localhost:8000

Endpoints:

## Registration

- `/api/sign-up/`

Expected:
>POST

```
{
  "username":"some_username",
  "password":"some_password",
  "name":"Some Name"
}
```
Optional JSON field:
```
"picture":"https://picture.url"
```

## Login

- `/api/sign-up/`

Expected:
>POST

```
{
  "username":"user_username",
  "password":"user_password"
}
```

Return:

```
{
  "token":"0sa54d54000some_token00a0b0n000"
}
```

## List articles

- `/api/articles/` (list of all articles)
- `/api/articles/?category=:slug` (list of articles of <:slug> category) 

Expected:
>GET

Return:
```
[
  {
    "id": "article's id",
    "author": {
      "id": "author's id",
      "name": "author's name",
      "picture": "authors picture url"
    },
    "category": "article's category",
    "title": "article's title",
    "summary": "article's summary"
  },
  ...
]
```

## Article details

- `/api/articles/:id/`

#### Anonymous user:

Expected:
>GET

Return:
```
{
  "id": "article's id",
  "author": {
    "id": "author's id",
    "name": "author's name",
    "picture": "authors picture url"
  },
  "category": "article's category",
  "title": "article's title",
  "summary": "article's summary",
  "firstParagraph": "article's first paragraph"
}
```

#### Logged user:

Expected:
>GET

Token informed when user logged in as **HEADER**:

>***Header NAME:***
>
>Authorization
>
>***Header VALUE:***
>
>token 0sa54d54000some_token00a0b0n000

Return:
```
{
  "id": "article's id",
  "author": {
    "id": "author's id",
    "name": "author's name",
    "picture": "authors picture url"
  },
  "category": "article's category",
  "title": "article's title",
  "summary": "article's summary",
  "firstParagraph": "article's first paragraph",
  "body": "article's body"
}
```

## Administrator restricted APIs

To access this feature it is necessary to have administrative rights (use the superuser account) and inform the token returned when logged in as **HEADER** on all requests.:

>***Header NAME:***
>
>Authorization
>
>***Header VALUE:***
>
>token 0sa54d54000some_token00a0b0n000
<br>

- `/api/admin/authors/`

>GET

Lists all authors. (currently listing all registered users)

Return:

```
[
  {
    "id": "id",
    "name": "author's name",
    "picture": "author's picture url
  },
  ...
]
```

>POST

Expected:

```
{
  "username":"some_username",
  "password":"some_password",
  "name":"Some Name"
}
```

Optional JSON field:

```
"picture":"https://picture.url"
```

---

- `/api/admin/authors/:id/`

>GET

Lists the details of the informed author via it's <:id>.

Return:

```
{
  "id": "id",
  "name": "author's name",
  "picture": "author's picture url
}
```

>PUT

Expected:

```
{
  "username":"some_username",
  "password":"some_password",
  "name":"Some Name"
}
```

>DELETE

Deletes informed author's <:id> **user** from the database.

---

- `/api/admin/articles/`

>GET

Lists all articles.

Return:

```
[
  {
  "id": "article's id",
  "author": "author's user id"
  "category": "article's category",
  "title": "article's title",
  "summary": "article's summary",
  "firstParagraph": "article's first paragraph",
  "body":"article's body"
  },
  ...
]
```

>POST

Expected:

```
{
  "author": "author's user id",
  "category": "category",
  "title": "title",
  "summary": "summary",
  "firstParagraph": "first paragraph",
  "body":"body"
}
```

---

- `/api/admin/articles/:id/`

>GET

Lists the details of the informed article via it's <:id>

Return:

```
{
  "id": "article's id",
  "author": "author's user id"
  "category": "article's category",
  "title": "article's title",
  "summary": "article's summary",
  "firstParagraph": "article's first paragraph",
  "body":"article's body"
}
```

>PUT

Expected:

```
{
  "author": "author's user id",
  "category": "category",
  "title": "title",
  "summary": "summary",
  "firstParagraph": "first paragraph",
  "body":"body"
}
```

>DELETE

Deletes informed article (via <:id>) from the database.

## Notes

In order to populate the database for testing purposes, you can either do it via the `/api/admin/` routes or, better yet, via Django's own admin layout, `localhost:8000/admin/` logging in with the superuser credentials.
