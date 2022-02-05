# Описание
### Польза миру
Может стать частью вашего блога с публикациями, подписками, сообществами.  
В проекте реализованы модели Comment, Follow, Group, Post и взаимодействие с ними по API.

### Учебные цели
Проект позволил на практике использовать знания REST Fraimwork и Django
такие как:
* настройка Models, обращения к БД через ORM
* настройка Serializers, валидация полей, переопределение связанных полей
* настройка ViewSets, permissions, переопределение методов get_queryset, perform_create
* настройка Routers в urls, версионирование API через URLPathVersioning
* управление нагрузкой на сервер через throttling
* применение pagination и filters в ответах по API
* настройка аутентификации через JSON Web Token (JWT)

# Установка и запуск

Клонировать репозиторий и перейти в него в командной строке:

```
git clone ...
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

# Примеры обращений по API
### Получить список статей, модель Post
запрос:
```
GET http://127.0.0.1:8000/api/v1/posts/ HTTP/1.1
Content-Type: application/json
```
ответ:
```
HTTP/1.1 200 OK
Date: Fri, 04 Feb 2022 15:46:03 GMT
Server: WSGIServer/0.2 CPython/3.7.12
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 124

[
  {
    "id": 1,
    "pub_date": "2022-02-03T17:33:31.901908Z",
    "author": "Fedor",
    "text": "Пост 1",
    "group": "science"
  },
  {
    "id": 2,
    "pub_date": "2022-02-03T17:33:31.901908Z",
    "author": "Fedor",
    "text": "Пост 2",
    "group": "filosophy"
  }
]
```
### Создать статью, модель Post
запрос:
```
POST http://127.0.0.1:8000/api/v1/posts/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer ...

{
    "text": "Пост 2",
    "group": "filosophy"
}
```
ответ:
```
HTTP/1.1 201 Created
Date: Fri, 04 Feb 2022 16:00:55 GMT
Server: WSGIServer/0.2 CPython/3.7.12
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 103

{
  "id": 2,
  "pub_date": "2022-02-04T16:00:55.819201Z",
  "author": "tm",
  "text": "Пост 2",
  "group": "filosophy"
}
```
### Получить статью, модель Post
запрос:
```
GET http://127.0.0.1:8000/api/v1/posts/2/ HTTP/1.1
Content-Type: application/json
```
ответ:
```
HTTP/1.1 200 OK
Date: Fri, 04 Feb 2022 16:36:25 GMT
Server: WSGIServer/0.2 CPython/3.7.12
Content-Type: application/json
Vary: Accept
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 103

{
  "id": 2,
  "pub_date": "2022-02-04T16:00:55.819201Z",
  "author": "tm",
  "text": "Пост 2",
  "group": "filosophy"
}
```
### Получить список сообществ, модель Group
запрос:
```
GET http://127.0.0.1:8000/api/v1/groups/ HTTP/1.1
Content-Type: application/json
```
ответ:
```
HTTP/1.1 200 OK
Date: Fri, 04 Feb 2022 16:40:23 GMT
Server: WSGIServer/0.2 CPython/3.7.12
Content-Type: application/json
Vary: Accept
Allow: GET, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 177

[
  {
    "id": 1,
    "title": "Наука",
    "slug": "science",
    "description": ""
  },
  {
    "id": 2,
    "title": "Философия",
    "slug": "filosophy",
    "description": "Статьи про философию"
  }
]
```
### Получить список комментариев к статье, модель Comment
запрос:
```
GET http://127.0.0.1:8000/api/v1/posts/1/comments/ HTTP/1.1
Content-Type: application/json
```
ответ:
```
HTTP/1.1 200 OK
Date: Fri, 04 Feb 2022 19:07:46 GMT
Server: WSGIServer/0.2 CPython/3.7.12
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 223

[
  {
    "id": 1,
    "post": 1,
    "author": "tm",
    "text": "Комментарий раз",
    "created": "2022-02-04T17:31:57.639198Z"
  },
  {
    "id": 2,
    "post": 1,
    "author": "tm",
    "text": "Комментарий два",
    "created": "2022-02-04T19:06:56.991368Z"
  }
]
```
### Создать комментариий к статье, модель Comment
запрос:
```
POST http://127.0.0.1:8000/api/v1/posts/1/comments/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer ...
```
ответ:
```
HTTP/1.1 201 Created
Date: Fri, 04 Feb 2022 19:09:56 GMT
Server: WSGIServer/0.2 CPython/3.7.12
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 112

{
  "id": 3,
  "post": "1",
  "author": "tm",
  "text": "Комментарий три",
  "created": "2022-02-04T19:09:56.068371Z"
}
```
### Получить список подписок на автора, модель Follow
запрос:
```
GET http://127.0.0.1:8000/api/v1/follow/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer ...
```
ответ:
```
TTP/1.1 200 OK
Date: Fri, 04 Feb 2022 19:14:21 GMT
Server: WSGIServer/0.2 CPython/3.7.12
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 35

[
  {
    "user": "tm",
    "following": "fedor"
  }
]
```
### Создать подписку на автора, модель Follow
запрос:
```
POST http://127.0.0.1:8000/api/v1/follow/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer ...
```
ответ:
```
HTTP/1.1 201 Created
Date: Fri, 04 Feb 2022 19:36:24 GMT
Server: WSGIServer/0.2 CPython/3.7.12
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 37

{
  "user": "fedor",
  "following": "teodor"
}
```
### Получить токен JWT, библиотека djoser
запрос:
```
POST http://127.0.0.1:8000/api/v1/jwt/create/ HTTP/1.1
Content-Type: application/json

{
    "username": "teodor",
    "password": "example"
}
```
ответ:
```
HTTP/1.1 200 OK
Date: Fri, 04 Feb 2022 19:28:26 GMT
Server: WSGIServer/0.2 CPython/3.7.12
Content-Type: application/json
Vary: Accept
Allow: POST, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 438

{
  "refresh": "eyJ0eXAiOiJKV1QiL88hbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NDA4OTMwNiwianRpIjoiYTZiMDY1OWNmO993NGNkYWI4ZDFmYTlmNGI2YjBhY2YiLCJ1c2VyX2lkIjozfQ.7H_CJ3G_-UvbhuSlLCf37wyezfxiZjS_dTqokgsv89E",
  "access": "eyJ0eXAiOiJKV1QiL88hbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ0MDg5MzA2LCJqdGkiOiJmNmI0N2FkYTI599U0MWY3YTQ2NmU4NjZjYmRiMWFiMCIsInVzZXJfaWQiOjN9.3vHaZgtHtUtVUpwy2JIU-7RU9iyvJD-Jj3HLPtxALRQ"
}
```

### Другие примеры запросов
Будут доступны после установки и запуска приложения по адресу:
```
your_domain.com/api/
```