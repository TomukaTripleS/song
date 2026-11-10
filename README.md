# Song

REST API каталогу пісень на Django REST Framework і SQLite. Реєстрація та JWT працюють у застосунку `accounts`.

## Запуск

Потрібен Python 3.12 або новіший.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

У Windows активуйте середовище командою `.venv\Scripts\activate`. Тести запускаються командою `python manage.py test`.

## API

Базова адреса — `http://127.0.0.1:8000/api/`. Для JSON-запитів передавайте `Content-Type: application/json`, для захищених запитів — `Authorization: Bearer <access>`.

| Метод і шлях | Тіло запиту | Відповідь |
| --- | --- | --- |
| POST `/register/` | Поля реєстрації нижче | `201` користувач, `400` помилки полів |
| POST `/token/` | `{"username":"student","password":"study-password-2026"}` | `200` `{"access":"...","refresh":"..."}`, `400` відсутні або порожні поля, `401` неправильні облікові дані |
| POST `/token/refresh/` | `{"refresh":"..."}` | `200` `{"access":"..."}`, `400` відсутній або порожній refresh, `401` недійсний refresh |
| GET `/me/` | Без тіла, з access-токеном | `200` поточний користувач, `401` потрібен дійсний access |

Для реєстрації потрібні `username` (унікальний, до 150 символів), `email` (коректна адреса до 254 символів), `password` (8–128 символів) і `password_confirmation` (до 128 символів, має збігатися з паролем). `first_name` і `last_name` необов’язкові, до 150 символів кожне.

```json
{
  "username": "student",
  "email": "student@example.com",
  "password": "study-password-2026",
  "password_confirmation": "study-password-2026"
}
```

Реєстрація та `/me/` повертають `{"id":1,"username":"student","email":"student@example.com","first_name":"","last_name":""}`. Пароль зберігається як хеш. Після реєстрації виконайте логін.

Access діє 5 хвилин, refresh — 1 добу. Коли access прострочується, клієнт отримує `401`, надсилає refresh на `/token/refresh/` і повторює запит із новим access. Якщо refresh недійсний, увійдіть знову. При виході клієнт видаляє обидва токени.

## Каталог

`{resource}` — `artists` або `songs`, `{id}` — ID запису. Перегляд публічний, для створення, редагування й видалення потрібен access-токен.

| Метод і шлях | Відповідь |
| --- | --- |
| GET `/{resource}/` | `200` список |
| GET `/{resource}/{id}/` | `200` об’єкт |
| POST `/{resource}/` | `201` створений об’єкт |
| PATCH `/{resource}/{id}/` | `200` оновлений об’єкт |
| DELETE `/{resource}/{id}/` | `204` без тіла |

Для створення виконавця передайте `name` (унікальний, до 150 символів). Для пісні потрібні `title` (до 200), `artist` (ID виконавця), `genre` (до 100) і `listen_url` (HTTP/HTTPS, до 500). `featured_date` необов’язкова, формат `YYYY-MM-DD` або `null`. Для `PATCH` передайте лише змінені поля. У відповідях також є `id`, а для пісні — `artist_name`.

`400` означає невалідні дані, `401` — відсутній або недійсний токен для зміни каталогу, `404` — запис або маршрут відсутній, `405` — метод не підтримується, `409` — у виконавця залишилися пісні. Приклад помилки реєстрації з деталями поля:

```json
{"error":{"message":"Перевірте правильність заповнення полів.","details":{"password_confirmation":["Паролі не збігаються."]}}}
```

## Postman

Запустіть колекцію зверху вниз з `base_url=http://127.0.0.1:8000`. Вона зберігає токени й ID автоматично. [Колекція Postman](postman/song.postman_collection.json)

Фронтенд працює окремо на порту `5500`. [Репозиторій фронтенду](https://github.com/TomukaTripleS/song-frontend)
