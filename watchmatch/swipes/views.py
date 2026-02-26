from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.db import models
from django.core.cache import cache

from rooms.models import Participant, Room
from .models import Swipe
from movies.models import Movie, Genre
from movies.services import (
    create_and_return_movie,
    get_movies_from_tmdb_by_room,
    get_movie_tmdb
)


def play_room(request, room_id, participant_id):
    """Комната для игры"""
    room = get_object_or_404(Room, id=room_id)
    participant = get_object_or_404(Participant, id=participant_id)
    participants = Participant.objects.filter(room_id=room)
    count_participants = participants.count()

    # Проверяем, есть ли уже выбранный фильм
    selected_movie_swipe = Swipe.objects.filter(room=room, status=True) \
                                        .values('movie') \
                                        .annotate(likes_count=models.Count('id')) \
                                        .order_by('-likes_count') \
                                        .first()

    if (selected_movie_swipe
            and selected_movie_swipe['likes_count'] >= count_participants):
        movie = get_object_or_404(Movie, id=selected_movie_swipe['movie'])
        context = {
            'room': room,
            'participant': participant,
            'movie': movie,
            'count_participants': count_participants,
            'participants': participants
        }
        return render(request, 'swipes/movie_selected.html', context)

    if request.method == "POST":
        movie_id = request.POST.get("movie_id")
        action = request.POST.get("action")

        movie_data = get_movie_tmdb(movie_id=int(movie_id))
        movie = create_and_return_movie(movie_data)

        Swipe.objects.update_or_create(
            participant=participant,
            movie=movie,
            room=room,
            defaults={"status": action == "like"},
        )

        return redirect(
            'swipes:play_room',
            room_id=room_id,
            participant_id=participant_id
        )

    cache_key = f"movies_for_room_{room.id}"
    movies_list = cache.get(cache_key)

    if not movies_list:
        movies_list = get_movies_from_tmdb_by_room(room)
        cache.set(cache_key, movies_list, timeout=60 * 120)

    swiped_movie_ids = Swipe.objects.filter(
        participant=participant,
        room=room
    ).values_list('movie_id', flat=True)

    unwatched_movies = [
        m for m in movies_list if m['id'] not in swiped_movie_ids
    ]

    if not unwatched_movies:
        movie = get_object_or_404(Movie, id=0)
    else:
        data = unwatched_movies[0]
        movie = create_and_return_movie(data)

    genre_ids = data.get('genre_ids', [])

    movie.genres.set(Genre.objects.filter(id__in=genre_ids))
    movie.save()

    context = {
        'room': room,
        'participant': participant,
        'movie': movie,
        'count_participants': count_participants,
        'participants': participants
    }

    return render(request, 'swipes/play_room.html', context)
