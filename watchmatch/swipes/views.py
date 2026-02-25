from django.shortcuts import get_object_or_404
from django.shortcuts import render

from rooms.models import Participant, Room


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
    template_name = 'swipes/play_room.html'
    return render(request, template_name, context)
