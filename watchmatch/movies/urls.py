from django.urls import path

from .views import detail_movie


urlpatterns = [
    path('<int:movie_id>', detail_movie, name='detail_movie'),
]
