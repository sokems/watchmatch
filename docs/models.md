# Сущности

1. **Room:**

|   Название поля    |                                              Тип                                              |        Описание        |
|:------------------:|:---------------------------------------------------------------------------------------------:|:----------------------:|
|         id         |                                             auto                                              |     Идентификатор      |
|        name        |                                   CharField(max_length=12)                                    |    Название комнаты    |
| count_participants |                                  PositiveSmallIntegerField()                                  | Количество участников  |
|       genres       |                         ManyToManyField(Genre, related_name='rooms')                          |    Выбранные жанры     |
|     year_start     |                                  PositiveSmallIntegerField()                                  |   Период релизов от    |
|      year_end      |                                  PositiveSmallIntegerField()                                  |   Период релизов до    |
|       adult        |                                        BooleanField()                                         |       Якорь 18+        |
|    vote_average    |                         DecimalField(max_digits=4, decimal_places=2)                          |  Минимальный рейтинг   |
|     is_playing     |                               models.BooleanField(default=True)                               |  Якорь активной игры   |
|    select_movie    | models.ForeignKey(Movie, verbose_name='Выбранный фильм', on_delete=models.CASCADE, null=True) | Фильм, который выбрали |


2. **Genre:**

| Название поля |              Тип               |         Описание         |
|:-------------:|:------------------------------:|:------------------------:|
|      id       | IntegerField(primary_key=True) | Идентификатор (TMDB API) |
|     name      |    CharField(max_length=50)    |   Название на русском    |


3. **Participant**

| Название поля |                                              Тип                                               |                     Описание                      |
|:-------------:|:----------------------------------------------------------------------------------------------:|:-------------------------------------------------:|
|      id       |                                              auto                                              |                   Идентификатор                   |
|     user      |           models.ForeignKey(User, verbose_name='Никнейм', on_delete=models.CASCADE)            |                   Имя участника                   |
|    room_id    | ForeignKey(Room, on_delete=models.CASCADE, related_name='participants', null=True, blank=True) | Идентификатор комнаты к которой подключился игрок |


4. **Movie**

| Название поля  |                            Тип                            |          Описание          |
|:--------------:|:---------------------------------------------------------:|:--------------------------:|
|       id       |              IntegerField(primary_key=True)               |  Идентификатор (TMDB API)  |
|     title      |           CharField(max_length=100, null=True)            | Название фильма на русском |
| original_title |           CharField(max_length=100, null=True)            |   Оригинальное название    |
|     genres     | ManyToManyField(Genre, related_name='movies', blank=True) |           Жанры            |
|  release_date  |                   DateField(null=True)                    |        Дата релиза         |
|     adult      |                  BooleanField(null=True)                  |         Якорь 18+          |
|  vote_average  |  DecimalField(max_digits=4, decimal_places=2, null=True)  |          Рейтинг           |
|    overview    |                   TextField(null=True)                    |          Описание          |
|  poster_path   |                    URLField(null=True)                    |        Путь постера        |
| backdrop_path  |                    URLField(null=True)                    |         Путь фона          |

5. **Swipe**

| Название поля |                                   Тип                                    |       Описание        |
|:-------------:|:------------------------------------------------------------------------:|:---------------------:|
|      id       |                              IntegerField()                              |     Идентификатор     |
|     room      |    ForeignKey(Room, on_delete=models.CASCADE, related_name='swipes')     | Идентификатор комнаты |
|     movie     |    ForeignKey(Movie, on_delete=models.CASCADE, related_name='swipes')    | Идентификатор фильма  |
|    status     |                        BooleanField(default=True)                        |      Like - True      |
|  participant  | ForeignKey(Participant, on_delete=models.CASCADE, related_name='swipes') |       Чей лайк        |

