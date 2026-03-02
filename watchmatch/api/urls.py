from django.urls import path, include

from .views import detail_movie, create_room

app_name = 'api'

urlpatterns_v1 = [
    path('movies/<int:movie_id>/', detail_movie, name='v1_detail_movie'),
    path('rooms/', create_room, name='v1_create_room'),
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1))
]