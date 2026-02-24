from django.shortcuts import render, redirect

from .forms import RoomForm, JoinRoomForm


def create_room(request):
    """Создание новой комнаты для игры"""
    template_name = 'rooms/create_room.html'
    form = RoomForm(request.POST or None)

    if form.is_valid():
        room = form.save()
        return redirect('rooms:play_room', room_id=room.id)

    context = {'form': form}

    return render(request, template_name, context)


def play_room(request, room_id):
    """Комната для игры"""
    context = {'room_id': room_id}
    template_name = 'rooms/play_room.html'
    return render(request, template_name, context)


def join_room(request):
    """Страница подключения к комнате"""
    template_name = 'rooms/join_room.html'

    if request.method == 'POST':
        form = JoinRoomForm(request.POST)

        if form.is_valid():
            room_id = form.cleaned_data['room_id']

            return redirect('rooms:play_room', room_id=room_id)
    else:
        form = JoinRoomForm()
        context = {'form': form}

    return render(request, template_name, context)
