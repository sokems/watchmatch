import warnings
import pytest

from django.test.client import Client
from django.urls import reverse

from movies.models import Movie, Genre
from rooms.models import Room, Participant
from swipes.models import Swipe


warnings.filterwarnings("ignore", category=DeprecationWarning)


# ================= CLIENT =================

@pytest.fixture
def client():
    return Client()


@pytest.fixture
def auth_user(django_user_model, db):
    return django_user_model.objects.create(username='sokem')


@pytest.fixture
def auth_user_client(auth_user):
    client = Client()
    client.force_login(auth_user)
    return client


@pytest.fixture
def admin_user(django_user_model):
    return django_user_model.objects.create_user(
        username='admin',
        password='password',
        is_staff=True,
        is_superuser=True
    )


@pytest.fixture
def admin_client(client, admin_user):
    client.login(username='admin', password='password')
    return client


# ================= URLS =================

@pytest.fixture
def url_admin_index():
    return reverse('admin:index')


@pytest.fixture
def url_homepage_index():
    return reverse('core:index')


@pytest.fixture
def url_about():
    return reverse('core:about')


@pytest.fixture
def url_create_room():
    return reverse('rooms:create_room')


@pytest.fixture
def url_join_room():
    return reverse('rooms:join_room')


@pytest.fixture
def url_list_rooms():
    return reverse('rooms:list_rooms')


@pytest.fixture
def url_list_movies():
    return reverse('movies:list_movies')


@pytest.fixture
def url_detail_movie(movie):
    return reverse('movies:detail_movie', kwargs={'movie_id': movie.pk})


@pytest.fixture
def url_play_room(room, participant):
    return reverse(
        'swipes:play_room',
        kwargs={
            'room_id': room.pk,
            'participant_id': participant.pk
        }
    )


# ================= GENRES =================

@pytest.fixture
def genre(db):
    return Genre.objects.create(id=1, name='Жанр 1')


@pytest.fixture
def genres(db):
    g1 = Genre.objects.create(id=1, name='Action')
    g2 = Genre.objects.create(id=2, name='Drama')
    return g1, g2


# ================= MOVIES =================

@pytest.fixture
def movie(db, genre):
    movie = Movie.objects.create(
        id=1,
        title='Фильм 1',
        original_title='Film 1',
        adult=False,
        vote_average=5,
        overview='Описание'
    )
    movie.genres.add(genre)
    return movie


@pytest.fixture
def mock_tmdb_movie(monkeypatch):
    def fake_get_movie_tmdb(movie_id):
        return {
            'id': movie_id,
            'title': 'Фильм 1',
            'original_title': 'Film 1',
            'genres': [{'id': 1, 'name': 'Жанр 1'}],
            'adult': False,
            'overview': 'Описание',
            'vote_average': 5,
        }
    monkeypatch.setattr('movies.views.get_movie_tmdb', fake_get_movie_tmdb)


@pytest.fixture
def mock_tmdb_list(monkeypatch):
    """Мокаем get_movie_tmdb для list_movies"""
    def fake_get_movie_tmdb(*args, **kwargs):
        # возвращаем фиктивный фильм
        return {
            "id": 1,
            "title": "Фильм 1",
            "genre_ids": [1],
            "adult": False,
            "overview": "Описание",
            "vote_average": 5,
            'original_title': 'Film 1',
        }
    monkeypatch.setattr("movies.views.get_movie_tmdb", fake_get_movie_tmdb)


@pytest.fixture
def movies(db, genres):
    g1, g2 = genres

    m1 = Movie.objects.create(id=1, title='Movie1')
    m2 = Movie.objects.create(id=2, title='Movie2')

    m1.genres.add(g1)
    m2.genres.add(g2)

    return m1, m2


# ================= ROOMS =================

@pytest.fixture
def room(db, genre):
    room = Room.objects.create(
        name='Комната 1',
        count_participants=2,
        year_start=2020,
        year_end=2021,
        adult=True,
        vote_average=5
    )
    room.genres.add(genre)
    return room


@pytest.fixture
def full_room(db, room, django_user_model):
    users = [
        django_user_model.objects.create(username='u1'),
        django_user_model.objects.create(username='u2')
    ]

    for u in users:
        Participant.objects.create(name=u, room_id=room)

    return room


# ================= PARTICIPANTS =================

@pytest.fixture
def participant(db, room, auth_user):
    return Participant.objects.create(name=auth_user, room_id=room)


@pytest.fixture
def participants(db, room, django_user_model, auth_user):
    u1 = auth_user
    u2 = django_user_model.objects.create(username='u2')

    p1 = Participant.objects.create(name=u1, room_id=room)
    p2 = Participant.objects.create(name=u2, room_id=room)

    return p1, p2


# ================= SWIPES =================

@pytest.fixture
def swipe_like(db, participant, movie, room):
    return Swipe.objects.create(
        room=room,
        movie=movie,
        participant=participant,
        status=True
    )


@pytest.fixture
def matched_movie(db, participants, movie, room):
    p1, p2 = participants

    Swipe.objects.create(room=room, movie=movie, participant=p1, status=True)
    Swipe.objects.create(room=room, movie=movie, participant=p2, status=True)

    return movie


# ================= FORM DATA =================

@pytest.fixture
def form_data_create_room(genre):
    return {
        'name': 'Комната2',
        'count_participants': 2,
        'genres': [genre.id],
        'year_start': 2020,
        'year_end': 2021,
        'adult': True,
        'vote_average': 5,
    }


@pytest.fixture
def form_data_create_room_valid(genres):
    g1, g2 = genres
    return {
        'name': 'Комната2',
        'count_participants': 2,
        'genres': [g1.id, g2.id],
        'year_start': 2020,
        'year_end': 2021,
        'adult': True,
        'vote_average': 5,
    }


@pytest.fixture
def form_data_join_valid(room):
    return {'room_id': room.pk}


@pytest.fixture
def form_data_join_invalid():
    return {'room_id': 9999}
