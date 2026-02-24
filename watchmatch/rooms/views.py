from django.shortcuts import render, redirect, get_object_or_404

from .forms import RoomForm, JoinRoomForm
from .models import Room, Participant


def create_room(request):
    """Создание новой комнаты для игры"""
    template_name = 'rooms/create_room.html'
    form = RoomForm(request.POST or None)

    if form.is_valid():
        room = form.save()

        Participant.objects.create(
            name=form.cleaned_data['creator_name'],
            room_id=room
        )

        return redirect('rooms:play_room', room_id=room.id)

    context = {'form': form}

    return render(request, template_name, context)


def play_room(request, room_id):
    """Комната для игры"""
    room = get_object_or_404(Room, pk=room_id)
    participants = Participant.objects.filter(room_id=room)
    count_participants = participants.count()

    context = {
        'room': room,
        'count_participants': count_participants,
        'participants': participants
    }
    template_name = 'rooms/play_room.html'
    return render(request, template_name, context)


def join_room(request):
    """Страница подключения к комнате"""
    template_name = 'rooms/join_room.html'
    form = JoinRoomForm(request.POST or None)

    if form.is_valid():
        room_id = form.cleaned_data['room_id']
        room = Room.objects.get(id=room_id)

        Participant.objects.create(
            name=form.cleaned_data['name'],
            room_id=room
        )

        return redirect('rooms:play_room', room_id=room_id)

    context = {'form': form}

    return render(request, template_name, context)
