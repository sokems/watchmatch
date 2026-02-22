from django.urls import path

from .views import detail_movie


app_name = 'movies'

urlpatterns = [
    path('<int:movie_id>', detail_movie, name='detail_movie'),
]
