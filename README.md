# Song

REST API каталогу пісень на Django REST Framework, база — SQLite.

## Як запустити проєкт

Python 3.12+:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

У Windows замість `source` виконайте `.venv\Scripts\activate`.
Бекенд: http://127.0.0.1:8000. База спочатку порожня.

## API

JSON, базова адреса `http://127.0.0.1:8000/api/`.
Замість `{resource}` використовуйте `artists` або `songs`.

| Метод | URL | Результат |
| --- | --- | --- |
| GET | `/{resource}/` | 200, список |
| POST | `/{resource}/` | 201, створений об’єкт |
| GET | `/{resource}/{id}/` | 200, об’єкт |
| PATCH | `/{resource}/{id}/` | 200, оновлений об’єкт |
| DELETE | `/{resource}/{id}/` | 204, без тіла |

Поля для створення (PATCH приймає лише змінені поля):

- `artists`: `name` — обов’язковий унікальний рядок до 150 символів.
- `songs`: `title` — рядок до 200 символів, `artist` — ID наявного виконавця, `genre` — рядок до 100 символів, `listen_url` — HTTP/HTTPS URL до 500 символів. Усі обов’язкові й непорожні. `featured_date` — необов’язкова дата `YYYY-MM-DD` або `null`.

`id` генерується автоматично; у відповіді пісні також є `artist_name`. Ці поля лише для читання.

Помилки: 400 — невалідні дані; 404 — об’єкт або маршрут відсутній; 405 — метод не підтримується.
409 — виконавець має пісні: видалення конфліктує зі станом бази. Спочатку видаліть пісні або змініть їхнього виконавця.

Єдиний формат помилки:

```json
{"error": {"message": "Повідомлення", "details": {}}}
```

## Postman і фронтенд

Імпортуйте [колекцію v2.1](postman/song.postman_collection.json), `base_url` = `http://127.0.0.1:8000`. Запускайте зверху вниз: ID зберігаються автоматично, наприкінці створені записи видаляються.

Фронтенд працює окремо на `http://127.0.0.1:5500`. CORS дозволяє цю адресу та `http://localhost:5500`.

Фронтенд: https://github.com/TomukaTripleS/song-frontend
