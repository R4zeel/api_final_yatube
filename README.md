# API для Yatube

## Описание
REST API для приложения-видеохостинга Yatube, реализован функционал запросов к группам контента, постам, комментариям и подпискам пользователей.
С доступными методами запросов для каждого из объектов можно ознакомиться в документации проекта.

## Установка
1. Клонируйте репозиторий на свой локальный компьютер
2. Установите виртуальное окружение
3. Установите зависимости из файла requirements.txt
4. Выполните миграции
5. Проект готов к работе

## Примеры
Ссылка на документацию - http://127.0.0.1:8000/redoc/
```
GET http://127.0.0.1:8000/api/v1/posts/
```
```
200 Response
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```
```
POST http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
Payload:
{
"text": "string"
}
```
```
201 Response
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2019-08-24T14:15:22Z",
  "post": 0
}
```


