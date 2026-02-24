from django.shortcuts import render
from django.conf import settings
import requests

from .models import Movie, Genre


def detail_movie(request, movie_id):
    """Страница фильма"""

    tmdb_api_key = settings.TMDB_API_KEY
    tmdb_url = (
        f"https://api.themoviedb.org/3/movie/"
        f"{movie_id}?api_key={tmdb_api_key}&language=ru-RU"
    )
    response = requests.get(tmdb_url)

    if response.status_code == 200:
        data = response.json()

        movie, created = Movie.objects.get_or_create(
            id=data['id'],
            defaults={
                'id': data['id'],
                'title': data['title'],
                'original_title': data['original_title'],
                'adult': data['adult'],
                'vote_average': data['vote_average'],
                'overview': data['overview'],
                'release_date': data.get('release_date'),
                'poster_path':
                    f"https://image.tmdb.org/t/p/original{data.get('poster_path')}",
                'backdrop_path':
                    f"https://image.tmdb.org/t/p/original{data.get('backdrop_path')}",
            }
        )

        genre_ids = []
        for g in data.get('genres', []):
            genre_obj, created = Genre.objects.get_or_create(
                id=g['id'], defaults={'name': g['name']}
            )
            genre_ids.append(genre_obj.id)

        movie.genres.set(Genre.objects.filter(id__in=genre_ids))
        movie.save()
    else:
        return render(request, 'movies/movie_not_found.html', status=404)

    context = {'movie': movie}
    template_name = 'movies/detail_movie.html'
    return render(request, template_name, context)
