import pytest
from django.shortcuts import reverse, redirect
from pytest_django.asserts import assertRedirects

from rooms.models import Room


@pytest.mark.django_db
def test_anonymous_can_create_room(client, form_data_create_room, genre):
    url = reverse('rooms:create_room')

    assert Room.objects.count() == 0

    response = client.post(url, data=form_data_create_room)

    room = Room.objects.get()
    assert room.participants.count() == 1
    participant = room.participants.first()

    expected_url = reverse(
        'swipes:play_room',
        args=(room.id, participant.id)
    )

    assertRedirects(response, expected_url)

    assert Room.objects.count() == 1
    assert room.name == form_data_create_room['name']
    assert room.count_participants == form_data_create_room['count_participants']
    assert room.year_start == form_data_create_room['year_start']
    assert room.year_end == form_data_create_room['year_end']
    assert room.adult == form_data_create_room['adult']
    assert room.vote_average == form_data_create_room['vote_average']
    assert room.genres.first() == genre


@pytest.mark.django_db
def test_anonymous_can_join_room(client, form_data_join_room, genre):
    url = reverse('rooms:join_room')

    assert Room.objects.count() == 1
    room = Room.objects.get()
    assert room.participants.count() == 0

    response = client.post(url, data=form_data_join_room)

    assert room.participants.count() == 1
    participant = room.participants.first()

    expected_url = reverse(
        'swipes:play_room',
        args=(room.id, participant.id)
    )

    assertRedirects(response, expected_url)

    assert Room.objects.count() == 1
    assert participant.name == form_data_join_room['name']
    assert room.id == form_data_join_room['room_id']
