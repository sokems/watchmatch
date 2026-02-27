import warnings

from django.test.client import Client
from django.urls import reverse
import pytest

from movies.models import Movie, Genre
from rooms.models import Room, Participant


warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest.fixture
def auth_user(django_user_model):
    """Создает зарегистрированного пользователя."""
    return django_user_model.objects.create(username='sokem')


@pytest.fixture
def auth_user_client(auth_user):
    """Возвращает клиент Django с авторизованным пользователем."""
    client = Client()
    client.force_login(auth_user)

    return client


@pytest.fixture
def url_admin_index():
    """Возвращает URL страницы админки."""
    return reverse('admin:index')


@pytest.fixture
def url_homepage_index():
    """Возвращает URL главной страницы"""
    return reverse('core:index')


@pytest.mark.django_db
@pytest.fixture
def genre():
    genre = Genre.objects.create(
        id=1,
        name='Жанр 1'
    )

    return genre


@pytest.mark.django_db
@pytest.fixture
def movie(genre):
    movie = Movie.objects.create(
        id=1,
        title='Фильм 1',
        original_title='Film 1',
        release_date=None,
        adult=False,
        vote_average=5,
        overview='Описание',
        poster_path=None,
        backdrop_path=None
    )

    movie.genres.add(genre)

    return movie


@pytest.mark.django_db
@pytest.fixture
def room(genre):
    room = Room.objects.create(
        name = 'Комната 1',
        count_participants = 1,
        year_start = 2020,
        year_end = 2021,
        adult = True,
        vote_average = 5
    )

    room.genres.add(genre)

    return room


@pytest.mark.django_db
@pytest.fixture
def participant(room):
    participant = Participant.objects.create(
        name='Роман',
        room_id=room
    )

    return participant


@pytest.fixture
def form_data_create_room(genre):
    return {
        'name': 'Комната2',
        'count_participants': 1,
        'year_start': 2020,
        'year_end': 2021,
        'adult': True,
        'vote_average': 5,
        'creator_name': 'Павел',
        'genres': [genre.id],
    }


@pytest.fixture
def form_data_join_room(room):
    return {
        'name': 'Рома',
        'room_id': room.pk
    }
