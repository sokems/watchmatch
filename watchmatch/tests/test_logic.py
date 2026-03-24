import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from rooms.models import Room, Participant


User = get_user_model()


@pytest.mark.django_db
def test_anonymous_cannot_create_room(client):
    """Анонимный пользователь не может создать комнату (редирект)."""
    url = reverse('rooms:create_room')

    response = client.post(url, {
        'name': 'Test Room',
        'count_participants': 2,
    })

    assert response.status_code == 302
    assert Room.objects.count() == 0


@pytest.mark.django_db
def test_auth_user_can_create_room(auth_user_client, genre):
    """Авторизованный пользователь может создать комнату."""
    url = reverse('rooms:create_room')

    response = auth_user_client.post(url, {
        'name': 'Test Room',
        'count_participants': 2,
        'genres': [genre.id],
        'year_start': 2000,
        'year_end': 2020,
        'adult': False,
        'vote_average': 7,
    })

    assert response.status_code == 302
    assert Room.objects.count() == 1


@pytest.mark.django_db
def test_anonymous_cannot_join_room(client, room):
    """Анонимный пользователь не может присоединиться к комнате (редирект)."""
    url = reverse('rooms:join_room')

    response = client.post(url, {
        'room_id': room.id
    })

    assert response.status_code == 302


@pytest.mark.django_db
def test_cannot_join_full_room(auth_user_client, room, django_user_model):
    """Нельзя присоединиться к полностью заполненной комнате."""
    room.count_participants = 1
    room.save()

    user = django_user_model.objects.create_user(username='mover')
    Participant.objects.create(name=user, room_id=room)

    room.refresh_from_db()

    assert room.participants.count() == 1
