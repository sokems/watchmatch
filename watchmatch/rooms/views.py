from django.shortcuts import render, redirect

from .forms import RoomForm, JoinRoomForm
from .models import Participant


def create_room(request):
    """Создание новой комнаты для игры"""
    template_name = 'rooms/create_room.html'
    form = RoomForm(request.POST or None)

    if form.is_valid():
        room = form.save()

        participant = Participant.objects.create(
            name=form.cleaned_data['creator_name'],
            room_id=room
        )

        return redirect(
            'swipes:play_room',
            room_id=room.id,
            participant_id=participant.id
        )

    context = {'form': form}

    return render(request, template_name, context)


def join_room(request):
    """Страница подключения к комнате"""
    template_name = 'rooms/join_room.html'
    form = JoinRoomForm(request.POST or None)

    if form.is_valid():
        room_id = form.cleaned_data['room_id']
        room = form.cleaned_data['room']

        participant = Participant.objects.create(
            name=form.cleaned_data['name'],
            room_id=room
        )

        return redirect(
            'swipes:play_room',
            room_id=room_id,
            participant_id=participant.id
        )

    context = {'form': form}

    return render(request, template_name, context)
