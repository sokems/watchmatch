import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from movies.models import Movie
from rooms.models import Room
from .serializers import MovieSerializer, RoomSerializer


logger = logging.getLogger(__name__)


@api_view(['GET'])
def detail_movie(request, movie_id):
    """
    Возвращает данные о фильме по его id в виде словаря
    """
    movie = Movie.objects.get(pk=movie_id)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(['POST'])
def create_room(request):
    """Создает новую комнату для игры"""
    serializer = RoomSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    logger.warning(
        f"Room creation failed. "
        f"Request data: {request.data}. "
        f"Validation errors: {serializer.errors}"
    )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
