# YaCut — короткие ссылки и загрузка файлов на Яндекс Диск

Flask-приложение, которое укорачивает длинные ссылки и загружает файлы на Яндекс Диск, выдавая на каждый файл короткую ссылку для скачивания.

## Возможности

- Короткая ссылка для любого URL: можно задать свой вариант или получить сгенерированный автоматически.
- Загрузка нескольких файлов за раз: файлы асинхронно отправляются на Яндекс Диск через REST API (aiohttp), и для каждого создаётся короткая ссылка. При переходе по ней сервис получает у Диска актуальную ссылку на скачивание и перенаправляет на неё.
- REST API: `POST /api/id/` создаёт короткую ссылку, `GET /api/id/<short_id>/` возвращает исходный URL. Спецификация — в `openapi.yml`.
- Валидация форм через Flask-WTF и понятные ответы при ошибках.

## Технологии

Python 3.10+, Flask, Flask-SQLAlchemy, Flask-Migrate (Alembic), Flask-WTF, aiohttp, SQLite, pytest.

## Как запустить

```bash
git clone https://github.com/Vantied/async-yacut.git
cd async-yacut
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Создайте файл `.env`:

```env
FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your_secret_key
DB=sqlite:///db.sqlite3
DISK_TOKEN=your_yandex_disk_oauth_token
```

```bash
flask db upgrade
flask run
```

Тесты: `pytest`.

## Что я вынес из проекта

- Асинхронные запросы к внешнему API внутри Flask-приложения.
- Веб-интерфейс и REST API поверх одной модели данных.

## Автор

Иван Богатов — [GitHub](https://github.com/Vantied) · Telegram [@Ivan_bogatov55](https://t.me/Ivan_bogatov55)
