from http import HTTPStatus

import pytest
from django.urls import reverse
from unittest.mock import patch

from rooms.forms import RoomForm, JoinRoomForm
from swipes.models import Swipe


@pytest.mark.django_db
def test_homepage_template(client, url_homepage_index):
    """Главная страница рендерится с шаблоном core/index.html."""
    response = client.get(url_homepage_index)

    assert response.status_code == HTTPStatus.OK
    assert 'core/index.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_create_room_contains_form(auth_user_client):
    """Страница создания комнаты содержит форму RoomForm."""
    url = reverse('rooms:create_room')
    response = auth_user_client.get(url)

    assert 'form' in response.context
    assert isinstance(response.context['form'], RoomForm)


@pytest.mark.django_db
def test_join_room_contains_form(auth_user_client):
    """Страница присоединения к комнате содержит форму JoinRoomForm."""
    url = reverse('rooms:join_room')
    response = auth_user_client.get(url)

    assert 'form' in response.context
    assert isinstance(response.context['form'], JoinRoomForm)


@pytest.mark.django_db
def test_room_detail_contains_participants(auth_user_client, participants, room):
    """Страница комнаты содержит корректных участников."""
    url = reverse('swipes:play_room', args=[room.pk, participants[0].pk])
    response = auth_user_client.get(url)

    assert 'room' in response.context
    assert response.context['room'] == room

    assert room.participants.count() == 2


@pytest.mark.django_db
def test_room_detail_displays_genres(auth_user_client, room, participants):
    """Страница комнаты отображает жанры."""
    url = reverse('swipes:play_room', args=[room.pk, participants[0].pk])
    response = auth_user_client.get(url)

    assert 'room' in response.context
    assert room.genres.exists()


@pytest.mark.django_db
def test_api_movie_detail(auth_user_client_token, movie, url_api_v1_movies_detail):
    """АПИ выдает верные поля по фильму"""
    response = auth_user_client_token.get(url_api_v1_movies_detail)

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['id'] == movie.id
    assert data['title'] == movie.title
    assert data['original_title'] == movie.original_title
    assert isinstance(data['genres'], list)
    assert data['genres'][0]['name'] == 'Жанр 1'
    assert data['adult'] == movie.adult
    assert float(data['vote_average']) == movie.vote_average
    assert data['overview'] == movie.overview


@pytest.mark.django_db
def test_api_random_movie(auth_user_client_token, url_api_v1_random_movie):
    """АПИ выдает случайный фильм"""
    response = auth_user_client_token.get(url_api_v1_random_movie)

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert 'title' in data
    assert 'original_title' in data
    assert 'genres' in data


@pytest.mark.django_db
def test_api_rooms_list(
        auth_user_client_token,
        room,
        room_without_participant,
        participant,
        url_api_v1_list_or_create_rooms
):
    """АПИ выдает список комнат, в которой состоит пользователь"""
    response = auth_user_client_token.get(url_api_v1_list_or_create_rooms)

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert len(data) == 1
    assert data[0]['id'] == room.id
    assert data[0]['name'] == room.name
    assert data[0]['count_participants'] == room.count_participants
    assert isinstance(data[0]['genres'], list)
    assert data[0]['genres'][0]['name'] == 'Жанр 1'
    assert data[0]['year_start'] == room.year_start
    assert data[0]['year_end'] == room.year_end
    assert data[0]['adult'] == room.adult
    assert float(data[0]['vote_average']) == room.vote_average
    assert data[0]['is_playing'] == room.is_playing
    assert data[0]['select_movie'] == room.select_movie


@pytest.mark.django_db
def test_api_room_detail(
        auth_user_client_token,
        room,
        participants,
        url_api_v1_detail_room
):
    """АПИ возвращает информацию о комнате"""
    response = auth_user_client_token.get(url_api_v1_detail_room)

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['id'] == room.id
    assert data['name'] == room.name
    assert data['count_participants'] == room.count_participants
    assert isinstance(data['genres'], list)
    assert data['genres'][0]['name'] == 'Жанр 1'
    assert data['year_start'] == room.year_start
    assert data['year_end'] == room.year_end
    assert data['adult'] == room.adult
    assert float(data['vote_average']) == room.vote_average
    assert data['is_playing'] == room.is_playing
    assert data['select_movie'] == room.select_movie

    assert len(data['participants']) == 2
    assert len(data['participants']) == room.count_participants
    assert participants[0].name.username in data['participants']


@pytest.mark.django_db
def test_api_swipe_first_movie(
    auth_user_client_token,
    room,
    participant,
    url_api_v1_swipe_movies
):
    """Проверка старта игры"""
    mock_movie_data = {
        'id': 1,
        'title': 'Фильм 1',
        'original_title': 'Film 1',
        'genres': [{'id': 1, 'name': 'Жанр 1'}],
        'adult': False,
        'overview': 'Описание',
        'vote_average': 5,
        'genre_ids': [1],
    }

    with patch(
            'api.v1.views.get_movies_from_tmdb_by_room',
            return_value=[mock_movie_data]
    ):
        response = auth_user_client_token.post(url_api_v1_swipe_movies, data={})

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert 'next_movie' in data
    assert 'title' in data['next_movie']
    assert 'genres' in data['next_movie']


@pytest.mark.django_db
def test_api_swipe_like(
    auth_user_client_token,
    room,
    participant,
    url_api_v1_swipe_movies
):
    """Проверка свайпа"""

    mock_movie_data = {
        'id': 1,
        'title': 'Фильм 1',
        'original_title': 'Film 1',
        'genres': [{'id': 1, 'name': 'Жанр 1'}],
        'adult': False,
        'overview': 'Описание',
        'vote_average': 5,
    }

    with patch('api.v1.views.get_movie_tmdb', return_value=mock_movie_data):
        response = auth_user_client_token.post(
            url_api_v1_swipe_movies,
            data={
                'movie_id': 1,
                'action': 'like'
            }
        )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert 'next_movie' in data or 'selected_movie' in data


@pytest.mark.django_db
def test_api_swipe_match(
        auth_user_client_token,
        room,
        participants,
        movie,
        url_api_v1_swipe_movies
):
    """Когда фильм выбран"""
    p1, p2 = participants

    Swipe.objects.create(room=room, movie=movie, participant=p1, status=True)
    Swipe.objects.create(room=room, movie=movie, participant=p2, status=True)

    mock_movie_data = {
        'id': movie.id,
        'title': movie.title,
        'original_title': movie.title,
        'genres': [{'id': 1, 'name': 'Жанр 1'}],
        'adult': False,
        'overview': 'Описание',
        'vote_average': 5,
        'release_date': '2020-01-01',
        'poster_path': '/poster.jpg',
        'backdrop_path': '/backdrop.jpg'
    }

    with patch(
            'api.v1.views.get_movies_from_tmdb_by_room',
            return_value=[mock_movie_data]
    ), \
            patch(
                'api.v1.views.create_and_return_movie',
                return_value=movie
            ):
        response = auth_user_client_token.post(url_api_v1_swipe_movies, data={
            'movie_id': movie.id,
            'action': 'like'
        })

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert 'selected_movie' in data
    assert data['selected_movie']['id'] == movie.id
    assert data['message'] == 'Фильм выбран!'
