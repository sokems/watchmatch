import pytest
from django.urls import reverse

from rooms.forms import RoomForm, JoinRoomForm


@pytest.mark.django_db
def test_homepage_template(client, url_homepage_index):
    """Главная страница рендерится с шаблоном core/index.html."""
    response = client.get(url_homepage_index)

    assert response.status_code == 200
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
