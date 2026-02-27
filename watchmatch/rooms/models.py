from django.db import models
from django.contrib.auth import get_user_model

from .validators import (
    validate_participants_count,
    validate_vote_average,
    validate_year
)
from movies.models import Movie


User = get_user_model()


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

    name = models.CharField(
        max_length=12,
        verbose_name='Название',
        help_text='не должно превышать 12 символов'
    )
    count_participants = models.PositiveSmallIntegerField(
        verbose_name='Количество участников',
        help_text='от 1 до 4 участников',
        validators=(validate_participants_count,)
    )
    genres = models.ManyToManyField(
        'movies.Genre',
        related_name='rooms',
        verbose_name='Жанры'
    )
    year_start = models.PositiveSmallIntegerField(
        verbose_name='Релиз от',
        help_text='Укажите начальный год релиза. Если нужен только один год, '
                  'укажите одинаковые значения в полях "Релиз от" и "Релиз до"',
        validators=(validate_year,)
    )
    year_end = models.PositiveSmallIntegerField(
        verbose_name='Релиз до',
        help_text='Укажите конечный год релиза',
        validators=(validate_year,)
    )
    adult = models.BooleanField(
        verbose_name='18+',
    )
    vote_average = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name='Средний рейтинг',
        help_text='Средний рейтинг по TMDB',
        validators=(validate_vote_average,)
    )
    is_playing = models.BooleanField(default=True)
    select_movie = models.ForeignKey(
        Movie,
        verbose_name='Выбранный фильм',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = 'комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return f'{self.pk} - {self.name} ({self.count_participants})'


class Participant(models.Model):
    """
    Участник комнаты.

    Представляет пользователя, участвующего в совместном голосовании
    за фильмы внутри комнаты.
    """

    name = models.ForeignKey(
        User,
        verbose_name='Никнейм',
        on_delete=models.CASCADE
    )

    room_id = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='participants',
        null=True,
        blank=True,
        verbose_name='ID комнаты',
    )

    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return f'{self.pk} - {self.name}'
