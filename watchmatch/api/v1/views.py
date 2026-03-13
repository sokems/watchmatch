import logging

from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from movies.models import Movie, Genre
from movies.services import get_movie_tmdb, create_and_return_movie
from rooms.models import Room, Participant
from .serializers import MovieSerializer, RoomReadSerializer, RoomListSerializer, RoomWriteSerializer
from .permissions import IsParticipant


logger = logging.getLogger(__name__)


class MovieDetailViewSet(mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    Получение фильма по ID
    или рандомный фильм
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

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
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    Создание и просмотр комнаты
    """

    queryset = Room.objects.all()


    def get_queryset(self):
        if self.action == 'list':
            return Room.objects.filter(participants__name=self.request.user)
        return super().get_queryset()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsParticipant]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return RoomWriteSerializer
        elif self.action == 'list':
            return RoomListSerializer
        return RoomReadSerializer

    def perform_create(self, serializer):
        room = serializer.save()
        Participant.objects.create(name=self.request.user, room_id=room)
