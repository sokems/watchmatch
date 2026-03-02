import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response

from movies.models import Movie
from rooms.models import Room
from .serializers import MovieSerializer, RoomSerializer


logger = logging.getLogger(__name__)


class MovieDetail(generics.RetrieveAPIView):
    """
    Возвращает данные о фильме по его id в виде словаря
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class CreateRoom(generics.CreateAPIView):
    """Создает новую комнату для игры"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
