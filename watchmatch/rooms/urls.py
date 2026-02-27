from django.urls import path

from .views import create_room, join_room, list_play_rooms


app_name = 'rooms'

urlpatterns = [
    path('create-room/', create_room, name='create_room'),
    path('join-room/', join_room, name='join_room'),
    path('list_rooms', list_play_rooms, name='list_rooms'),
]
