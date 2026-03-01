import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from .forms import RoomForm, JoinRoomForm
from .models import Participant, Room


User = get_user_model()
logger = logging.getLogger(__name__)


@login_required
def create_room(request):
    """Создание новой комнаты для игры"""
    template_name = 'rooms/create_room.html'
    form = RoomForm(request.POST or None)

    if form.is_valid():
        room = form.save()
        user = request.user

        participant = Participant.objects.create(
            name=user,
            room_id=room
        )

        return redirect(
            'swipes:play_room',
            room_id=room.id,
            participant_id=participant.id
        )

    if form.errors:
        logger.warning(f"Failed to create room by user {request.user.id}: {form.errors}")

    context = {'form': form}

    return render(request, template_name, context)


@login_required
def join_room(request):
    """Страница подключения к комнате"""
    template_name = 'rooms/join_room.html'
    form = JoinRoomForm(request.POST or None)

    if form.is_valid():
        room_id = form.cleaned_data['room_id']
        room = form.cleaned_data['room']
        user = request.user

        participant = Participant.objects.create(
            name=user,
            room_id=room
        )

        logger.info(f"User {user.id} joined room {room_id} as participant {participant.id}")

        return redirect(
            'swipes:play_room',
            room_id=room_id,
            participant_id=participant.id
        )

    if form.errors:
        logger.warning(f"User {request.user.id} failed to join room: {form.errors}")

    context = {'form': form}

    return render(request, template_name, context)


@login_required
def list_play_rooms(request):
    """
    Отображает список комнат,
    в которой состоит пользователь
    """
    template_name = 'rooms/list_rooms.html'
    rooms = Room.objects.filter(participants__name=request.user).distinct()

    participants_dict = {
        room.id: room.participants.get(name=request.user)
        for room in rooms
    }

    context = {
        'rooms': rooms,
        'participants_dict': participants_dict
    }

    return render(request, template_name, context)
