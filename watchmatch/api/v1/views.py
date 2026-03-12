import logging

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from movies.models import Movie
from rooms.models import Room, Participant
from .serializers import MovieSerializer, RoomSerializer


logger = logging.getLogger(__name__)


class MovieDetailViewSet(mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    Только просмотр фильма по ID
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


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
