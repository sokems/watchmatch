import random

from django.conf import settings
import requests

from .models import Movie


def get_movie_tmdb(movie_id=None) -> dict:
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
