from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Форма для регистрации
    """
    email = forms.EmailField(required=True, help_text="Введите корректный email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class GetTokenForm(forms.Form):
    """
    Форма для получения API токена
    """
    username = forms.CharField(
        label='Ник',
        help_text='имя, которое используете для входа'
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput()
    )
