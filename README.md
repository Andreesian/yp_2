# Документация
### Получение списка всех групп
Возвращает список всех групп
```
GET http://0.0.0.0:8080/groups
```
Примерный ответ:
```
[
    {
        "description": "default_description",
        "id": 2,
        "name": "default"
    },
    {
        "description": "default_description",
        "id": 3,
        "name": "default"
    }
]
```
### Добавление группы
Добавляет группу в общий список
```
POST http://0.0.0.0:8080/group
```
Примерный запрос:
```
{
    "name":"default",
    "description":"default_description"
}
```
Примерный ответ:
```
{
    "id": 3
}
```
### Получение полной информации о группе
Возвращает полную информацию запрашиваемой группы
```
POST http://0.0.0.0:8080/group/{id}
```
Примерный ответ:
```
{
    {
    "description": "default_description",
    "id": 2,
    "name": "default",
    "participants": [
        {
            "id": 4,
            "name": "person",
            "recipient": {
                "id": 5,
                "name": "person2",
                "wish": "none"
            },
            "wish": "gift"
        },
        {
            "id": 5,
            "name": "person2",
            "recipient": {
                "id": 6,
                "name": "person2",
                "wish": "none"
            },
            "wish": "none"
        },
        {
            "id": 6,
            "name": "person2",
            "recipient": {
                "id": 4,
                "name": "person",
                "wish": "gift"
            },
            "wish": "none"
        }
    ]
}
```
### Изменение данных группы
Изменяет данные запрашиваемой группы
```
PUT http://0.0.0.0:8080/group/{id}
```
Примерный запрос:
```
{
    "name":"changed",
    "description":"changed_description"
}
```
Примерный ответ:
```
{
    "status": "success"
}
```
### Удаление группы
Удаляет запрашиваемую группу
```
DELETE http://0.0.0.0:8080/group/{id}
```
Примерный ответ:
```
{
    "status": "success"
}
```
### Добавление участника
Добавляет нового участника в запрашиваемую группу
```
POST http://0.0.0.0:8080/group/{id}/participant
```
Примерный запрос:
```
{
    "name":"person",
    "wish":"gift"
}
```
Примерный ответ:
```
{
    "id": 4
}
```
### Удаление участника
Удаляет заданного участника из запрашиваемой группы
```
DELETE http://0.0.0.0:8080/group/{group_id}/participant/{participant_id}
```
Примерный ответ:
```
{
   "status": "success"
}
```
### Распределение получателей среди участников
Проводит распределение в запрашиваемой группе и возвращает результаты
```
POST http://0.0.0.0:8080/group/{id}/toss
```
Примерный ответ:
```
[
    {
        "id": 4,
        "name": "person",
        "recipient": {
            "id": 5,
            "name": "person2",
            "wish": "none"
        },
        "wish": "gift"
    },
    {
        "id": 5,
        "name": "person2",
        "recipient": {
            "id": 6,
            "name": "person2",
            "wish": "none"
        },
        "wish": "none"
    },
    {
        "id": 6,
        "name": "person2",
        "recipient": {
            "id": 4,
            "name": "person",
            "wish": "gift"
        },
        "wish": "none"
    }
]
```
### Просмотр получателя участника
Возвращает получателя у заданного участника в запрашиваемой группе
```
POST http://0.0.0.0:8080/group/{group_id}/participant/{participant_id}/recipient
```
Примерный ответ:
```
{
    "id": 6,
    "name": "person2",
    "wish": "none"
}
```
