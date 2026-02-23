from django import forms

from movies.models import Genre
from .models import Room


class RoomForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        label='Название комнаты',
        help_text='не должно превышать 100 символов'
    )
    count_participants = forms.IntegerField(
        min_value=1,
        max_value=4,
        label='Количество участников',
        help_text='от 1 до 4 участников'
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Жанр',
    )
    year_start = forms.IntegerField(
        label='Релиз от',
        help_text='Укажите начальный год релиза. Если нужен только один год, '
                  'укажите одинаковые значения в полях "Релиз от" и "Релиз до"'
    )
    year_end = forms.IntegerField(
        label='Релиз до',
    )
    adult = forms.BooleanField(
        required=False,
        label='18+'
    )
    vote_average = forms.DecimalField(
        max_digits=4,
        decimal_places=2,
        min_value=0,
        max_value=10,
        label='Рейтинг от',
        required=False,
    )

    class Meta:
        model = Room
        fields = [
            'name',
            'count_participants',
            'genres',
            'year_start',
            'year_end',
            'adult',
            'vote_average',
        ]