from django.shortcuts import render


def detail_movie(request, movie_id):
    """Страница фильма"""
    template_name = 'movies/detail_movie.html'
    return render(request, template_name)
