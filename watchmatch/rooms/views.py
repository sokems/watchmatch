from django.shortcuts import render


def create_room(request):
    """Создание новой комнаты для игры"""
    template_name = 'rooms/create_room.html'
    return render(request, template_name)


def play_room(request, room_id):
    """Комната для игры"""
    context = {'room_id': room_id}
    template_name = 'rooms/play_room.html'
    return render(request, template_name, context)


def join_room(request):
    """Страница подключения к комнате"""
    template_name = 'rooms/join_room.html'
    return render(request, template_name)
