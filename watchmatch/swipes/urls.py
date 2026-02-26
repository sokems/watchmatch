from django.urls import path

from .views import play_room


app_name = 'swipes'

urlpatterns = [
    path('<int:room_id>/<int:participant_id>', play_room, name='play_room'),
]