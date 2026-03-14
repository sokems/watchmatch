![WatchMatch Logo](./watchmatch/static_dev/img/logo.png)

For Russian version see [README.md](README.md)

## Description

**WatchMatch** is a web application that helps a group of people choose a movie or cartoon for watching together using a swipe-based system.

Users join a shared room where the creator sets filters, and then swipe through movies. If all participants like a movie, a match occurs.

---

## MVP Features

- Create a room with filters:
  - Genres
  - Release year
  - Rating
  - 18+ content
  - Number of participants
- Join a room using an ID
- View the list of participants and room filters
- Swipe movies (like/dislike)
- Detect matches and display the result

---

## Target Audience

- Friends
- Couples
- Families
- Small groups up to 4 people

---

## Tech Stack

- Python 3.12
- Django 6.0.2
- Django Bootstrap 5
- MySQL
- TMDB API (fetch movies, genres, posters, descriptions)
- Python-dotenv
- Django Debug Toolbar
- Requests
- Django REST Framework (DRF)
- drf-yasg (Swagger / OpenAPI)

---

## Installation & Setup

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/watchmatch.git
cd watchmatch
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Create a .env file and add your keys:

```
SECRET_KEY='<your_django_secret_key>'
DEBUG=True
DB_NAME=<db_name>
DB_USER='<db_user>'
DB_PASSWORD='<db_password>'
DB_HOST='<db_host>'
DB_PORT=<db_port>
TMDB_API_KEY='<your_tmdb_api_key>'
EMAIL_HOST_USER='<email_for_smtp>'
EMAIL_HOST_PASSWORD='<password_email>'
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Apply migrations:

```bash
python manage.py migrate
```

6. Run the server:

```bash
python manage.py runserver
```

7. Open your browser at: http://127.0.0.1:8000

---

## External Services Used

- **TMDB API** — for fetching movies, genres, posters, and descriptions

---

## Project Structure (Minimum Entities)

- **Room** — Voting room
- **Participant** — Room participant
- **Movie** — Movie from TMDB
- **Swipe** — User vote for a movie
- **Genre** — Movie genre

---

## Development & Testing Tools

- PyCharm
- Pytest / Pytest-Django (testing)
- Flake8 (static code analysis)

---

## API

The project provides a REST API for interacting with the application.

Main endpoints:

- GET /api/v1/movies/random — get a random movie
- GET /api/v1/movies/{id}/ — get a movie by ID
- GET /api/v1/rooms/ — get the list of rooms the user belongs to
- POST /api/v1/rooms/ — create a room
- GET /api/v1/rooms/{id}/ — get room information
- POST /api/v1/rooms/{id}/swipe — perform a movie swipe action

API documentation:
- /redoc