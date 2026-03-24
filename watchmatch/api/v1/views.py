import logging

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from movies.models import Movie, Genre
from movies.services import (
    get_movie_tmdb,
    create_and_return_movie,
    get_movies_from_tmdb_by_room
)
from rooms.models import Room, Participant
from .serializers import (
    MovieSerializer,
    RoomReadSerializer,
    RoomListSerializer,
    RoomWriteSerializer,
    SwipeActionSerializer
)
from .permissions import IsParticipant
from swipes.models import Swipe


logger = logging.getLogger(__name__)


class MovieDetailViewSet(mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    Получение фильма.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получить фильм по ID",
        operation_description="Детальная информация о фильме."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить случайный фильм",
        operation_description="Детальная информация о случайном фильме."
    )
    @action(methods=['get'], detail=False)
    def random(self, request):
        """Получение случайного фильма."""
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
    """Механика комнаты"""

    queryset = Room.objects.all()

    @swagger_auto_schema(
        operation_summary="Список комнат",
        operation_description="Возвращает список комнат в которой состоит пользователь."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать комнату",
        operation_description="Регистрация новой комнаты с обязательной валидацией.",
        responses={201: RoomWriteSerializer(many=False)}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить комнату по ID",
        operation_description="Детальная информация о конкретной комнате."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        if self.action == 'list':
            return Room.objects.filter(participants__name=self.request.user).distinct()
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
    def join(self, request, pk=None):
        """
        Подключение пользователя к комнате
        """
        room = get_object_or_404(Room, pk=pk)

        if room.participants.count() >= room.count_participants:
            return Response(
                {"message": "Комната заполнена."},
                status=status.HTTP_403_FORBIDDEN
            )

        participant, created = Participant.objects.get_or_create(
            name=request.user,
            room_id=room
        )
        if not created:
            return Response(
                {"message": "Вы уже подключены к этой комнате."},
                status=status.HTTP_200_OK
            )

        return Response(
            {"message": f"Вы успешно подключились к комнате {room.id}."},
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        operation_summary="Свайп в комнате (лайк/дизлайк фильма)",
        operation_description="""
        **Основная механика игры**:
        - Без параметров: только первый запрос к эндпоинту
        - С `movie_id` + `action` ('like'/'dislike'):
        сохраняет свайп и проверяет выбор фильма всеми участниками
        - При достижении консенсуса — фильм выбран для просмотра
        """,
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description="Уникальный ID комнаты (автоинкремент)",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'movie_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID фильма из TMDB'
                ),
                'action': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['like', 'dislike'],
                    description='Действие над фильмом'
                ),
            },
            required=[]
        ),
        responses={
            200: openapi.Response(
                'Следующий фильм или выбранный фильм',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'next_movie': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'title': openapi.Schema(type=openapi.TYPE_STRING),
                                'genres': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_STRING
                                    )
                                ),
                                'release_date': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format=openapi.FORMAT_DATE
                                ),
                                'vote_average': openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT
                                ),
                                'adult': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                            }
                        ),
                        'selected_movie': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'title': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        ),
                        'message': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
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
            swiped_ids = Swipe.objects.filter(
                participant=participant,
                room=room
            ).values_list('movie_id', flat=True)
            unwatched = [m for m in movies_list if m['id'] not in swiped_ids]
            if not unwatched:
                return Response(
                    {
                        'next_movie': None,
                        'message': 'Нет доступных фильмов для этой комнаты.'
                    }
                )
            next_data = unwatched[0]
            next_movie = create_and_return_movie(next_data)
            next_movie.genres.set(
                Genre.objects.filter(
                    id__in=next_data.get(
                        'genre_ids', []
                    )
                )
            )
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

        swiped_ids = Swipe.objects.filter(
            participant=participant,
            room=room
        ).values_list('movie_id', flat=True)
        unwatched = [m for m in movies_list if m['id'] not in swiped_ids]

        if not unwatched:
            return Response(
                {
                    'next_movie': None,
                    'message': 'Нет доступных фильмов для этой комнаты.'
                }
            )

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
