import logging

from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

from movies.models import Movie, Genre
from movies.services import get_movie_tmdb, create_and_return_movie
from rooms.models import Room, Participant
from .serializers import MovieSerializer, RoomSerializer


logger = logging.getLogger(__name__)


class MovieDetailViewSet(mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    Получение фильма по ID
    или рандомный фильм
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(methods=['get'], detail=False)
    def random(self, request):
        """Получение рандомного фильма"""
        data = get_movie_tmdb()
        movie = create_and_return_movie(data)
        genre_ids = data.get('genre_ids', [])

        movie.genres.set(Genre.objects.filter(id__in=genre_ids))
        movie.save()
        serializer = MovieSerializer(movie)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RoomViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    Создание и просмотр комнаты
    """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    #permission_classes = [IsAuthenticated]

    def get_participant(self):
        return Participant.objects.get(name=self.request.user)

    def get_queryset(self):
        user = self.get_participant()
        return Room.objects.filter(participants=user)

    def perform_create(self, serializer):
        room = serializer.save()
        participant = Participant.objects.create(name=self.request.user, room_id=room)
