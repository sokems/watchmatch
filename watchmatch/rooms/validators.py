from decimal import Decimal

from django.core.exceptions import ValidationError


def validate_participants_count(value: int):
    if value < 1 or value > 4:
        raise ValidationError('Количество участников может быть от 1 до 4')


def validate_vote_average(value: Decimal):
    if value < 0 or value > 10:
        raise ValidationError('Рейтинг может быть от 0 до 10')


def validate_year(value):
    if value < 0:
        raise ValidationError('Нельзя указать год до нашей эры')
