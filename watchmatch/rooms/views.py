from django.http import HttpResponse


def create_room(request):
    """Создание новой комнаты для игры"""
    return HttpResponse('Создание комнаты')


def play_room(request, room_id):
    """Комната для игры"""
    return HttpResponse(f'Комната с id: {room_id}')


def join_room(request):
    """Страница подключения к комнате"""
    return HttpResponse('Введите id комнаты')
