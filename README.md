![WatchMatch Logo](./watchmatch/static_dev/img/logo.png)
Для английской версии смотрите [README_EN.md](README_EN.md)
## Описание

**WatchMatch** — веб-приложение, которое помогает группе людей выбрать фильм или мультфильм для совместного просмотра через систему свайпов.

Пользователи подключаются к общей комнате, где создатель задаёт фильтры, и свайпают фильмы. Если фильм нравится всем участникам — происходит мэтч.

---

## Функционал MVP

- Создание комнаты с фильтрами:
  - Жанры
  - Год выпуска
  - Рейтинг
  - 18+
  - Количество участников
- Подключение участников по ID комнаты
- Просмотр списка участников и фильтров комнаты
- Свайп фильмов (лайк/дизлайк)
- Определение совпадений (match) и показ результата

---

## Целевая аудитория

- Друзья
- Пары
- Семьи
- Компании до 4 человек

---

## Технологический стек

- Python 3.12
- Django 6.0.2
- Django Bootstrap 5
- MySQL
- TMDB API (получение фильмов, жанров, постеров и описаний)
- Python-dotenv
- Django Debug Toolbar
- Requests

---

## Установка и запуск

1. Клонируем репозиторий:

```bash
git clone https://github.com/<your-username>/watchmatch.git
cd watchmatch
```

2. Создаём виртуальное окружение и активируем его:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Создаем файл .env и вставляем ключи:

```
SECRET_KEY='<ваш_ключ_django>'
DEBUG=True
DB_NAME=<db_name>
DB_USER='<db_user>'
DB_PASSWORD='<db_password>'
DB_HOST='<db_host>'
DB_PORT=<db_port>
TMDB_API_KEY='<ваш_ключ_tmdb_api>'
EMAIL_HOST_USER='<email_для_smtp>'
EMAIL_HOST_PASSWORD='<пароль_email>'
```

4. Устанавливаем зависимости:

```bash
pip install -r requirements.txt
```

5. Применяем миграции:

```bash
python manage.py migrate
```

6. Запускаем сервер:

```bash
python manage.py runserver
```

7. Переходим в браузере по адресу: `http://127.0.0.1:8000`

---

## Используемые внешние сервисы

- **TMDB API** — получение фильмов, жанров, постеров и описаний

---

## Структура проекта (минимальные сущности)

- **Room** — Комната голосования
- **Participant** — Участник комнаты
- **Movie** — Фильм из TMDB
- **Swipe** — Голос пользователя за фильм
- **Genre** — Жанр фильма

---

## Инструменты разработки и тестирования

- PyCharm
- Pytest / Pytest-Django (тестирование)
- Flake8 (статический анализ кода)