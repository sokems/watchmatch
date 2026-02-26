from django.shortcuts import render

from .models import Genre
from .services import get_movie_tmdb, create_and_return_movie


def detail_movie(request, movie_id):
    """Страница фильма"""

    data = get_movie_tmdb(movie_id)

    if not data or 'id' not in data:
        return render(request, "movies/movie_not_found.html", status=404)

    movie = create_and_return_movie(data)

    genre_ids = []
    for g in data.get('genres', []):
        genre_obj = Genre.objects.get_or_create(
            id=g['id'], defaults={'name': g['name']}
        )[0]
        genre_ids.append(genre_obj.id)

    movie.genres.set(Genre.objects.filter(id__in=genre_ids))
    movie.save()

    return render(request, 'movies/detail_movie.html', {'movie': movie})


def list_movies(request):
    """Страница случайного фильма"""
    data = get_movie_tmdb()

    movie = create_and_return_movie(data)

    genre_ids = data.get('genre_ids', [])

    movie.genres.set(Genre.objects.filter(id__in=genre_ids))
    movie.save()

    return render(request, 'movies/list_movies.html', {"movie": movie})
