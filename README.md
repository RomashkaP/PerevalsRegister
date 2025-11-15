# Pereval API

Задача данного проекта заключалась в разработке API для мобильного   
приложения, которое представляет собой электронный реестр  
перевалов Росии.

В ходе разработки были реализованы 4 метода.

- `POST` Метод для отправки информации о перевале на сервер.
- `GET` Метод для получения информации о перевале по его `id`
- `GET` Метод для получения информации о всех перевалах отдельного  
пользователя по `email` пользователя.
- `PATCH` Метод для обновления информации о перевале по его `id` и с условием того,  
что его статус - `new`.


---
## Содержание

- [Аутентификация](#authentication)
- [Описание эндпоинтов](#endpointsdiscription)
  - [POST /submitData](#postsubmitdata)
  - [GET /submitData/{id}](#getsubmitdata)
  - [GET /submitData/ ?user__email=email](#getemail)
  - [PATCH /submitData/{id}](#pathsubmitdata)
- [Формат ответов](#responsesformat)
- [Примеры запросов](#requestexamples)


---

<a id="authentication"></a>
## Аутентификация

На данный момент API **не требует аутентификации**.  
Все запросы можно отправлять без токенов.

---

<a id="endpointsdiscription"></a>
## Описание эндпоинтов

<a id="postsubmitdata"><a/>
### POST /submitData 

- Создаёт новый перевал.

#### Тело запроса:
```python
{
    "pereval_area": 0,
    "beauty_title": "string",
    "title": "string",
    "other_titles": "string",
    "connects": "string",
    "user": 0,
    "coords": {
        "id": 0,
        "latitude": 0,
        "longitude": 0,
        "height": 0
    },
    "winter": "string",
    "spring": "string",
    "summer": "string",
    "autumn": "string",
    "activity_type": 0,
    "images": []
}
```

#### Ответ:
```python
{
    'status': 'succes',
    'id': pereval_id
}
```
<a id="getsubmitdata"></a>
### GET /submitData/{id}
- Получает перевал по указанному `id`.

#### Параметры URL:

- `pereval_id` (int, required) - ID перевала.

#### Ответ: 
```python
{
  "id": 1,
  "pereval_area": {
    "id": 1,
    "region": {
        "id": 1,
        "title": "string"
      },
    "title": "string"
  },
  "beauty_title": "string",
  "title": "string",
  "other_titles": "string",
  "connects": "string",
  "add_time": "2025-11-04T18:24:18.970166+03:00",
  "user": {
    "id": 1,
    "email": "string",
    "phone_num": "string",
    "surname": "string",
    "name": "string",
    "patronymic": "string"
  },
  "coords": { 
    "id": 3,
    "latitude": 1.2,
    "longitude": 1.2,
    "height": 12
  },
  "winter": "1A",
  "spring": "1A",
  "summer": "1A",
  "autumn": "1A",
  "activity_type": {
    "id": 1,
    "title": "string"
  },
  "images": [],
  "status": "new"
}
```

<a id="getemail"></a>
### GET /submitData/?user__email=example@email.com

- Получает все записи перевалов пользователя (список словарей) по указанному email.

#### Параметры URL: 

- `email` (str, reqired) - email пользователя.

#### Ответ: 

```python
[
  {
  "id": 1,
  "pereval_area": {
    "id": 1,
    "region": {
        "id": 1,
        "title": "string"
      },
    "title": "string"
  },
  "beauty_title": "string",
  "title": "string",
  "other_titles": "string",
  "connects": "string",
  "add_time": "2025-11-04T18:24:18.970166+03:00",
  "user": {
    "id": 1,
    "email": "string",
    "phone_num": "string",
    "surname": "string",
    "name": "string",
    "patronymic": "string"
  },
  "coords": { 
    "id": 3,
    "latitude": 1.2,
    "longitude": 1.2,
    "height": 12
  },
  "winter": "1A",
  "spring": "1A",
  "summer": "1A",
  "autumn": "1A",
  "activity_type": {
    "id": 1,
    "title": "string"
  },
  "images": [],
  "status": "new"
  },
  {
    ...
  },
  {
    ...
  }
]
```

<a id="pathsubmitdata"></a>
### PATCH /submitData/{id}

- Обновляет данные перевала, `id` которого указано в запросе и если  
его статус - `new`.

#### Параметры URL:

- `id` (int, requered) - ID перевала.

#### Тело запроса:

```python
{
  "pereval_area": 0,
  "beauty_title": "string",
  "title": "string",
  "other_titles": "string",
  "connects": "string",
  "user": 0,
  "coords": {
    "id": 0,
    "latitude": 0,
    "longitude": 0,
    "height": 0
  },
  "winter": "string",
  "spring": "string",
  "summer": "string",
  "autumn": "string",
  "activity_type": 0,
  "images": []
}
```

#### Ответ:

```python
{
  'state': 1, 
  'message': 'Запись успешно отредактирована.'
 }
```
#### Или:

```python
{
  'state': 0, 
  'message': 'Не удалось обновить запись (статус не "new" или запись не найдена)'
 }
```

---

<a id="responsesformat"></a>
### Формат ответов

Все ответы возвращаются в формате json.

#### Успешные ответы:
- `200 OK` - запрос обработан успешно. 

#### Ошибки:
- `400 Bad Request` - ошибка в данных запроса.
- `422 Validation Error` - ошибка валидации Pydentic.

---

<a id="requestexamples"></a>
### Примеры запросов

- POST /submitData:

#### Запрос: 
```bush
curl -X 'POST' \
  'http://127.0.0.1:8003/submitData/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "pereval_area": 1,
  "beauty_title": "string",
  "title": "string",
  "other_titles": "string",
  "connects": "string",
  "user": 1,
  "coords": {
    "id": 0,
    "latitude": 65.123456,
    "longitude": 65.123456,
    "height": 600
  },
  "winter": "1A",
  "spring": "1A",
  "summer": "1A",
  "autumn": "1A",
  "activity_type": 1,
  "images": []
}'
```

#### Ответ:

```bush
{
  "status": "success",
  "id": 31
}
```

- GET /submitData/{pereval_id} 

#### Запрос:
```bush
curl -X 'GET' \
  'http://127.0.0.1:8003/submitData/1' \
  -H 'accept: application/json'
```

#### Ответ:
```bush
{
  "id": 1,
  "pereval_area": {
    "id": 1,
    "region": {
      "id": 1,
      "title": "Алтай"
    },
    "title": "Семинский"
  },
  "beauty_title": "string",
  "title": "TEST PATCH 2",
  "other_titles": "string",
  "connects": "string",
  "add_time": "2025-11-04T18:24:18.970166+03:00",
  "user": {
    "id": 1,
    "email": "panichevr@gmail.com",
    "phone_num": "+79040456894",
    "surname": "Паничев",
    "name": "Роман",
    "patronymic": "Владимирович"
  },
  "coords": {
    "id": 3,
    "latitude": 1.2,
    "longitude": 1.2,
    "height": 12
  },
  "winter": "1A",
  "spring": "1A",
  "summer": "1A",
  "autumn": "1A",
  "activity_type": {
    "id": 1,
    "title": "Пешком"
  },
  "images": [],
  "status": "new"
}
```

- GET/submitData/?user__email=example@email.com

#### Запрос:
```bush
curl -X 'GET' \
  'http://127.0.0.1:8003/submitData/?user__email=panichevr%40gmail.com' \
  -H 'accept: application/json'
```

#### Ответ:
```bush
[
  {
    "id": 3,
    "pereval_area": {
      "id": 1,
      "region": {
        "id": 1,
        "title": "Алтай"
      },
      "title": "Семинский"
    },
    "beauty_title": null,
    "title": "Кату-Ярык",
    "other_titles": "",
    "connects": "Долину реки Чулышман с внешним миром.",
    "add_time": "2025-11-09T10:43:38.001449+03:00",
    "user": {
      "id": 1,
      "email": "panichevr@gmail.com",
      "phone_num": "+79040456894",
      "surname": "Паничев",
      "name": "Роман",
      "patronymic": "Владимирович"
    },
    "coords": {
      "id": 5,
      "latitude": 50.909958,
      "longitude": 88.217849,
      "height": 515
    },
    "winter": "1B",
    "spring": "1B",
    "summer": "2B",
    "autumn": "1A",
    "activity_type": {
      "id": 1,
      "title": "Пешком"
    },
    "images": [],
    "status": "new"
  },
  ,
  {
    "id": 5,
    ...
   },
   {
    ...
   }
]
```

- PATCH /submitData/{id}

### Запрос:
```bush
curl -X 'PATCH' \
  'http://127.0.0.1:8003/submitData/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "pereval_area": 1,
  "beauty_title": "string",
  "title": "string",
  "other_titles": "string",
  "connects": "string",
  "user": 1,
  "coords": {
    "id": 1,
    "latitude": 33.333333,
    "longitude": 33.333333,
    "height": 333
  },
  "winter": "1A",
  "spring": "1A",
  "summer": "1A",
  "autumn": "1A",
  "activity_type": 1,
  "images": []
}'
```

#### Ответ:
```bush
{
  "state": 1,
  "message": "Запись успешно отредактирована."
}
```

---
## Пиимечания

Этот проект создан в рамках курса python-разработчик  
от онлайн университета SkillFactory.  
Любые замечания и предложения приветствуются.