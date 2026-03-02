from django.urls import path, include

from .views import detail_movie

app_name = 'api'

urlpatterns_v1 = [
    path('movies/<int:movie_id>', detail_movie, name='detail_movie'),
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1))
]