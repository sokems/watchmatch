from django.db import models


class Swipe(models.Model):
    """
    Голосование (swipe) за фильм внутри комнаты.

    Модель фиксирует реакцию участников комнаты на конкретный фильм.
    Используется в механике совместного выбора фильма (аналог Tinder-swipe).

    Связи:
    - room — комната, в которой происходит голосование
    - movie — фильм, за который голосуют участники

    Поля:
    - status — итоговое решение по фильму:
        True  — фильм принят (match)
        False — фильм отклонён
    - count_likes — количество лайков от участников комнаты

    Логика работы:
    Когда число лайков достигает количества участников комнаты,
    фильм считается выбранным и формируется match.
    """

    room = models.ForeignKey(
        'rooms.Room',
        on_delete=models.CASCADE,
        related_name='swipes',
    )
    movie = models.ForeignKey(
        'movies.Movie',
        on_delete=models.CASCADE,
        related_name='swipes',
    )
    status = models.BooleanField(default=True)
    count_likes = models.PositiveSmallIntegerField()
