from django.shortcuts import render


def detail_movie(request, movie_id):
    """Страница фильма"""
    context = {'movie_id': movie_id}
    template_name = 'movies/detail_movie.html'
    return render(request, template_name, context)
