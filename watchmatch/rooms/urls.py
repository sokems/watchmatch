from django.urls import path

from .views import create_room, play_room, join_room


app_name = 'rooms'

urlpatterns = [
    path('create-room/', create_room, name='create_room'),
    path('join-room/', join_room, name='join_room'),
    path('join-room/<int:room_id>/', play_room, name='play_room'),
]
