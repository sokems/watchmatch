from django.shortcuts import render

from .models import Movie


def detail_movie(request, movie_id):
    """Страница фильма"""
    movie = Movie.objects.get(pk=movie_id)
    context = {'movie': movie}
    template_name = 'movies/detail_movie.html'
    return render(request, template_name, context)
