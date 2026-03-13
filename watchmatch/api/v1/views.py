import logging

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.core.cache import cache

from movies.models import Movie, Genre
from movies.services import get_movie_tmdb, create_and_return_movie, get_movies_from_tmdb_by_room
from rooms.models import Room, Participant
from .serializers import MovieSerializer, RoomReadSerializer, RoomListSerializer, RoomWriteSerializer, SwipeActionSerializer
from .permissions import IsParticipant
from swipes.models import Swipe


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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def swipe(self, request, pk=None):
        room = get_object_or_404(Room, pk=pk)
        participant = get_object_or_404(Participant, room_id=room, name=request.user)

        cache_key = f'movies_for_room_{room.id}'
        movies_list = cache.get(cache_key)
        if not movies_list:
            movies_list = get_movies_from_tmdb_by_room(room)
            cache.set(cache_key, movies_list, timeout=60*120)

        serializer = SwipeActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie_id = serializer.validated_data.get('movie_id')
        action = serializer.validated_data.get('action')

        if not movie_id and not action:
            swiped_ids = Swipe.objects.filter(participant=participant, room=room).values_list('movie_id', flat=True)
            unwatched = [m for m in movies_list if m['id'] not in swiped_ids]
            if not unwatched:
                return Response({'next_movie': None, 'message': 'Нет доступных фильмов для этой комнаты.'})
            next_data = unwatched[0]
            next_movie = create_and_return_movie(next_data)
            next_movie.genres.set(Genre.objects.filter(id__in=next_data.get('genre_ids', [])))
            next_movie.save()
            return Response({
                'next_movie': {
                    'id': next_movie.id,
                    'title': next_movie.title,
                    'genres': [g.name for g in next_movie.genres.all()],
                    'release_date': next_movie.release_date,
                    'vote_average': next_movie.vote_average,
                    'adult': next_movie.adult
                }
            })

        movie_data = get_movie_tmdb(int(movie_id))
        movie = create_and_return_movie(movie_data)
        Swipe.objects.update_or_create(
            participant=participant,
            movie=movie,
            room=room,
            defaults={'status': action == 'like'}
        )

        count_participants = Participant.objects.filter(room_id=room).count()
        selected = Swipe.objects.filter(room=room, status=True) \
                                .values('movie') \
                                .annotate(likes_count=models.Count('id')) \
                                .order_by('-likes_count') \
                                .first()

        if selected and selected['likes_count'] >= count_participants:
            selected_movie = get_object_or_404(Movie, id=selected['movie'])
            room.is_playing = False
            room.select_movie = selected_movie
            room.save()
            return Response({
                'selected_movie': {
                    'id': selected_movie.id,
                    'title': selected_movie.title
                },
                'message': 'Фильм выбран!'
            })


        swiped_ids = Swipe.objects.filter(participant=participant, room=room).values_list('movie_id', flat=True)
        unwatched = [m for m in movies_list if m['id'] not in swiped_ids]

        if not unwatched:
            return Response({'next_movie': None, 'message': 'Нет доступных фильмов для этой комнаты.'})

        next_data = unwatched[0]
        next_movie = create_and_return_movie(next_data)
        genre_ids = next_data.get('genre_ids', [])
        next_movie.genres.set(Genre.objects.filter(id__in=genre_ids))
        next_movie.save()

        return Response({
            'next_movie': {
                'id': next_movie.id,
                'title': next_movie.title,
                'genres': [g.name for g in next_movie.genres.all()],
                'release_date': next_movie.release_date,
                'vote_average': next_movie.vote_average,
                'adult': next_movie.adult
            }
        })