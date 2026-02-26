import random

from django.conf import settings
import requests

from .models import Movie


def get_movie_tmdb(movie_id=None) -> dict:
    """
    Делает обращение к сервису TMDB,
    получает либо случайный фильм
    либо конкретный по movie_id.

    Возвращает словарь с данными фильма
    """
    if movie_id:
        url = (
            f"https://api.themoviedb.org/3/movie/"
            f"{movie_id}?"
            f"api_key={settings.TMDB_API_KEY}&"
            f"language=ru-RU"
        )

    else:
        page = random.randint(1, 500)

        url = (f"https://api.themoviedb.org/3/discover/movie?"
               f"api_key={settings.TMDB_API_KEY}&"
               f"page={page}&"
               f"language=ru-RU")

    response = requests.get(url)

    if response.status_code != 200:
        return {}

    data = response.json()

    if movie_id:
        return data
    else:
        movies = data.get("results", [])
        if not movies:
            return {}
        random_movie = random.choice(movies)
        return random_movie


def create_and_return_movie(data: dict) -> Movie:
    """
    Проверяет существование фильма в БД,
    при отсутствии создает его

    Возвращает объект Movie
    """
    release_date = data.get('release_date') or None

    movie = Movie.objects.get_or_create(
        id=data['id'],
        defaults={
            'title': data['title'],
            'original_title': data['original_title'],
            'adult': data['adult'],
            'vote_average': data['vote_average'],
            'overview': data['overview'],
            'release_date': release_date,
            'poster_path':
                f"https://image.tmdb.org/t/p/original{data.get('poster_path')}",
            'backdrop_path':
                f"https://image.tmdb.org/t/p/original{data.get('backdrop_path')}",
        }
    )[0]

    return movie


def get_movies_from_tmdb_by_room(room, count=50) -> list[dict]:
    """
    Возвращает список фильмов из TMDB по фильтрам комнаты.
    count - сколько фильмов нужно вернуть
    """
    genre_ids = ",".join(str(g.id) for g in room.genres.all())
    gte = min(room.year_start, room.year_end)
    lte = max(room.year_start, room.year_end)

    movies = []
    page = 1

    while page <= (count // 20) + 1:
        url = (
            "https://api.themoviedb.org/3/discover/movie?"
            f"api_key={settings.TMDB_API_KEY}&"
            f"with_genres={genre_ids}&"
            f"include_adult={str(room.adult).lower()}&"
            f"vote_average.gte={room.vote_average}&"
            f"language=ru-RU&"
            f"primary_release_date.gte={gte}-01-01&"
            f"primary_release_date.lte={lte}-12-31&"
            f"page={page}"
        )

        response = requests.get(url)
        if response.status_code != 200:
            break

        data = response.json()
        results = data.get("results", [])
        if not results:
            break

        movies.extend(results)
        page += 1

    return movies
