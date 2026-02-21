from django.http import HttpResponse


def detail_movie(request, movie_id):
    """Описание фильма"""
    return HttpResponse(f'Фильм с id: {movie_id}')
