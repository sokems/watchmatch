from django.db import models


class Genre(models.Model):
    """
    Жанр фильма.

    Используется для категоризации фильмов и фильтрации
    при создании комнаты.
    """

    id = models.IntegerField(
        primary_key=True,
        verbose_name='TMDB ID',
        help_text='Идентификатор с TMDB API (заполняется автоматически)'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
        help_text='Название жанра'
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


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

    id = models.IntegerField(
        primary_key=True,
        verbose_name='TMDB ID',
        help_text='Идентификатор с TMDB API (заполняется автоматически)'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Название',
        help_text='Название на русском языке',
        null=True
    )
    original_title = models.CharField(
        max_length=100,
        verbose_name='Оригинальное название',
        help_text='Название на языке оригинала',
        null=True
    )
    genres = models.ManyToManyField(
        Genre,
        related_name='movies',
        verbose_name='Жанр',
        null=True
    )
    release_date = models.DateField(
        verbose_name='Дата релиза',
        help_text='Дата релиза в мире',
        null=True
    )
    adult = models.BooleanField(
        verbose_name='18+',
        help_text='Контент с рейтингом 18+',
        null=True
    )
    vote_average = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name='Средний рейтинг',
        help_text='Средний рейтинг по TMDB',
        null=True
    )
    overview = models.TextField(
        verbose_name='Описание',
        help_text='Описание на русском языке',
        null=True
    )
    poster_path = models.URLField(
        verbose_name='URL постера',
        help_text='Открытый источник к постеру',
        null=True
    )
    backdrop_path = models.URLField(
        verbose_name='URL фона',
        help_text='Открытый источник к фону по фильму',
        null=True
    )

    class Meta:
        verbose_name = 'фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return f'{self.title} ({self.release_date})'
