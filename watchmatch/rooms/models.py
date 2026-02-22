from django.db import models


class Room(models.Model):
    """
    Комната для совместного подбора фильма.

    Пользователи создают комнату, где задают фильтры поиска фильмов:
    - количество участников
    - интересующие жанры
    - диапазон годов выпуска
    - ограничение 18+
    - минимальный рейтинг

    После создания комнаты участники голосуют за фильмы (механика swipe).
    """

    name = models.CharField(max_length=100)
    count_participants = models.PositiveSmallIntegerField()
    genres = models.ManyToManyField(
        'movies.Genre',
        related_name='rooms',
    )
    year_start = models.PositiveSmallIntegerField()
    year_end = models.PositiveSmallIntegerField()
    adult = models.BooleanField()
    vote_average = models.DecimalField(max_digits=4, decimal_places=2)


class Participant(models.Model):
    """
    Участник комнаты.

    Представляет пользователя, участвующего в совместном голосовании
    за фильмы внутри комнаты.
    """

    name = models.CharField(max_length=50)