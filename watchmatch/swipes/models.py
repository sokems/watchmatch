from django.db import models


class Swipe(models.Model):
    """
    Голосование (swipe) за фильм внутри комнаты.

    Модель фиксирует реакцию участников комнаты на конкретный фильм.
    Используется в механике совместного выбора фильма (аналог Tinder-swipe).

    Связи:
    - room — комната, в которой происходит голосование
    - movie — фильм, за который голосуют участники
    - participant - участник комнаты

    Поля:
    - status — итоговое решение по фильму:
        True  — фильм принят (match)
        False — фильм отклонён

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
    participant = models.ForeignKey(
        'rooms.Participant',
        on_delete=models.CASCADE,
        related_name='swipes'
    )
