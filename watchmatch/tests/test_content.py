from django.shortcuts import reverse
import pytest

from rooms.forms import RoomForm, JoinRoomForm


@pytest.mark.django_db
def test_create_room_page_contains_form(client):
    url = reverse('rooms:create_room')
    response = client.get(url)

    assert 'form' in response.context
    assert isinstance(response.context['form'], RoomForm)


@pytest.mark.django_db
def test_join_room_page_contains_form(client):
    url = reverse('rooms:join_room')
    response = client.get(url)

    assert 'form' in response.context
    assert isinstance(response.context['form'], JoinRoomForm)
