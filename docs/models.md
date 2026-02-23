# Сущности

1. **Room:**

|   Название поля    |                     Тип                      |       Описание        |
|:------------------:|:--------------------------------------------:|:---------------------:|
|         id         |                IntegerField()                |     Идентификатор     |
|        name        |          CharField(max_length=100)           |   Название комнаты    |
| count_participants |         PositiveSmallIntegerField()          | Количество участников |
|       genres       | ManyToManyField(Genre, related_name='rooms') |    Выбранные жанры    |
|     year_start     |         PositiveSmallIntegerField()          |   Период релизов от   |
|      year_end      |         PositiveSmallIntegerField()          |   Период релизов до   |
|       adult        |                BooleanField()                |       Якорь 18+       |
|    vote_average    | DecimalField(max_digits=4, decimal_places=2) |  Минимальный рейтинг  |


2. **Genre:**

| Название поля |              Тип               |         Описание         |
|:-------------:|:------------------------------:|:------------------------:|
|      id       | IntegerField(primary_key=True) | Идентификатор (TMDB API) |
|     name      |    CharField(max_length=50)    |   Название на русском    |


3. **Participant**

|   Название поля    |           Тип            |   Описание    |
|:------------------:|:------------------------:|:-------------:|
|         id         |      IntegerField()      | Идентификатор |
|        name        | CharField(max_length=50) | Имя участника |


4. **Movie**

| Название поля  |                      Тип                      |          Описание          |
|:--------------:|:---------------------------------------------:|:--------------------------:|
|       id       |        IntegerField(primary_key=True)         |  Идентификатор (TMDB API)  |
|     title      |           CharField(max_length=100)           | Название фильма на русском |
| original_title |           CharField(max_length=100)           |   Оригинальное название    |
|     genres     | ManyToManyField(Genre, related_name='movies') |           Жанры            |
|  release_date  |                  DateField()                  |        Дата релиза         |
|     adult      |                BooleanField()                 |         Якорь 18+          |
|  vote_average  | DecimalField(max_digits=4, decimal_places=2)  |          Рейтинг           |
|    overview    |                  TextField()                  |          Описание          |
|  poster_path   |                  URLField()                   |        Путь постера        |
| backdrop_path  |                  URLField()                   |         Путь фона          |

5. **Swipe**

| Название поля |                                Тип                                 |                                Описание                                |
|:-------------:|:------------------------------------------------------------------:|:----------------------------------------------------------------------:|
|      id       |                           IntegerField()                           |                             Идентификатор                              |
|     room      | ForeignKey(Room, on_delete=models.CASCADE, related_name='swipes')  |                         Идентификатор комнаты                          |
|     movie     | ForeignKey(Movie, on_delete=models.CASCADE, related_name='swipes') |                          Идентификатор фильма                          |
|    status     |                     BooleanField(default=True)                     | Статус голосования, если кто то поставил дизлайк, то меняется на false |
|  count_likes  |                    PositiveSmallIntegerField()                     |                           Количество лайков                            |

