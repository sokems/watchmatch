from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model

from rooms.models import Room, Participant


User = get_user_model()


@pytest.mark.django_db
def test_anonymous_cannot_create_room(client, url_create_room):
    """Анонимный пользователь не может создать комнату (редирект)."""
    response = client.post(url_create_room, {
        'name': 'Test Room',
        'count_participants': 2,
    })

    assert response.status_code == HTTPStatus.FOUND
    assert Room.objects.count() == 0


@pytest.mark.django_db
def test_auth_user_can_create_room(auth_user_client, genre, url_create_room):
    """Авторизованный пользователь может создать комнату."""
    response = auth_user_client.post(url_create_room, {
        'name': 'Test Room',
        'count_participants': 2,
        'genres': [genre.id],
        'year_start': 2000,
        'year_end': 2020,
        'adult': False,
        'vote_average': 7,
    })

    assert response.status_code == HTTPStatus.FOUND
    assert Room.objects.count() == 1


@pytest.mark.django_db
def test_anonymous_cannot_join_room(client, room, url_join_room):
    """Анонимный пользователь не может присоединиться к комнате (редирект)."""
    response = client.post(url_join_room, {
        'room_id': room.id
    })

    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_cannot_join_full_room(auth_user_client, room, django_user_model):
    """Нельзя присоединиться к полностью заполненной комнате."""
    room.count_participants = 1
    room.save()

    user = django_user_model.objects.create_user(username='mover')
    Participant.objects.create(name=user, room_id=room)

    room.refresh_from_db()

    assert room.participants.count() == 1


@pytest.mark.django_db
def test_api_only_authenticated_can_access_movies(
        auth_user_client_token,
        anonymous_client,
        movie,
        url_api_v1_movies_detail
):
    """
    Проверяет, что доступ к деталям фильма разрешен только авторизованным пользователям.
    """
    response_anon = anonymous_client.get(url_api_v1_movies_detail)
    assert response_anon.status_code == HTTPStatus.UNAUTHORIZED

    response_auth = auth_user_client_token.get(url_api_v1_movies_detail)
    assert response_auth.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_api_anonymous_cannot_create_room(
        anonymous_client,
        url_api_v1_list_or_create_rooms
):
    """Анонимный пользователь не может создать комнату через АПИ."""
    response = anonymous_client.post(url_api_v1_list_or_create_rooms, {
        'name': 'Test Room',
        'count_participants': 2,
    })

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert Room.objects.count() == 0


@pytest.mark.django_db
def test_api_auth_user_can_create_room(
        auth_user_client_token,
        genre,
        url_api_v1_list_or_create_rooms
):
    """Авторизованный пользователь может создать комнату через АПИ."""
    response = auth_user_client_token.post(url_api_v1_list_or_create_rooms, {
        'name': 'Test Room',
        'count_participants': 2,
        'genres': [genre.id],
        'year_start': 2000,
        'year_end': 2020,
        'adult': False,
        'vote_average': 7,
    })

    assert response.status_code == HTTPStatus.CREATED
    assert Room.objects.count() == 1


@pytest.mark.django_db
def test_api_anonymous_cannot_join_room(
        anonymous_client,
        room,
        url_api_v1_detail_room
):
    """Анонимный пользователь не может посмотреть комнату через АПИ."""
    response = anonymous_client.post(url_api_v1_detail_room, {
        'room_id': room.id
    })

    assert Room.objects.count() == 1
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.django_db
def test_api_cannot_join_full_room(
        auth_admin_client_token,
        room,
        participant,
        url_api_v1_join_room
):
    """Нельзя присоединиться к полностью заполненной комнате через АПИ."""
    room.count_participants = 1
    room.save()

    response = auth_admin_client_token.post(url_api_v1_join_room, {
        'room_id': room.id
    })

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert room.participants.count() == 1
