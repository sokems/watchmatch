from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MovieDetailViewSet, RoomViewSet

app_name = 'v1'
router_v1 = DefaultRouter()
router_v1.register('movies', MovieDetailViewSet, basename='movies')
router_v1.register('rooms', RoomViewSet, basename='rooms')


urlpatterns = [
    path('v1/', include(router_v1.urls))
]
