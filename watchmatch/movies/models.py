from django.db import models


class Genre(models.Model):
    """
    Жанр фильма.

    Используется для категоризации фильмов и фильтрации
    при создании комнаты.
    """

    name = models.CharField(max_length=50)


class Movie(models.Model):
    """
    Фильм, доступный для голосования.

    Хранит основную информацию о фильме:
    - названия
    - жанры
    - дату релиза
    - рейтинг
    - описание
    - ссылки на изображения

    Используется в механике swipe для совместного выбора фильма.
    """

    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    genres = models.ManyToManyField(
        Genre,
        related_name='movies',
    )
    release_date = models.DateField()
    adult = models.BooleanField()
    vote_average = models.DecimalField(max_digits=4, decimal_places=2)
    overview = models.TextField()
    poster_path = models.URLField()
    backdrop_path = models.URLField()
