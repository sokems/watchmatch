from django import forms
from django.core.validators import ValidationError

from movies.models import Genre
from .models import Room


class RoomForm(forms.ModelForm):
    """
    Форма для создания комнаты
    """
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
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genres'].queryset = Genre.objects.all()


class JoinRoomForm(forms.Form):
    """
    Форма для подключения к комнате
    """
    room_id = forms.IntegerField(
        label='ID комнаты',
        help_text='ID вам сообщит его создатель'
    )

    def clean(self):
        cleaned_data = super().clean()
        room_id = cleaned_data.get('room_id')

        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            raise ValidationError("Комната с таким ID не найдена.")

        if room.participants.count() >= room.count_participants:
            raise ValidationError("Комната заполнена, больше участников нельзя.")

        self.cleaned_data['room'] = room

        return cleaned_data
