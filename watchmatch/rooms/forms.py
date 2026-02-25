from django import forms

from movies.models import Genre
from .models import Room


class RoomForm(forms.ModelForm):
    creator_name = forms.CharField(
        max_length=50,
        label='Ваше имя',
        help_text='максимальное количество символов 50'
    )
    count_participants = forms.TypedChoiceField(
        choices=[(i, i) for i in range(1, 5)],
        coerce=int,
        label='Количество участников',
        help_text='от 1 до 4 участников'
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label='Жанр',
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
            'creator_name',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genres'].queryset = Genre.objects.all()

    def clean_creator_name(self):
        creator_name = self.cleaned_data['creator_name']
        return ''.join(creator_name.split())

    def clean_name(self):
        name = self.cleaned_data['name']
        return ''.join(name.split())


class JoinRoomForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        label='Имя',
        help_text='введите свое имя'
    )
    room_id = forms.IntegerField(
        label='ID комнаты',
        help_text='ID вам сообщит его создатель'
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        return ''.join(name.split())
