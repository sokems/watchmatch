from django.urls import path

from .views import detail_movie, list_movies


app_name = 'movies'

urlpatterns = [
    path('', list_movies, name='list_movies'),
    path('<int:movie_id>', detail_movie, name='detail_movie'),
]
