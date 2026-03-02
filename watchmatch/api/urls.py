from django.urls import path, include

from .views import MovieDetail, CreateRoom

app_name = 'api'

urlpatterns_v1 = [
    path('movies/<int:pk>/', MovieDetail.as_view(), name='v1_detail_movie'),
    path('rooms/', CreateRoom.as_view(), name='v1_create_room'),
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1))
]