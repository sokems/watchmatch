from rest_framework import serializers
from django.contrib.auth import get_user_model

from movies.models import Movie, Genre
from rooms.models import Room, Participant
from swipes.models import Swipe


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'original_title',
            'genres',
            'release_date',
            'adult',
            'vote_average',
            'overview',
            'poster_path',
            'backdrop_path'
        )


class RoomReadSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    participants = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = (
            'id',
            'name',
            'count_participants',
            'participants',
            'genres',
            'year_start',
            'year_end',
            'adult',
            'vote_average',
            'is_playing',
            'select_movie'
        )

    def get_participants(self, obj):
        participants = Participant.objects.filter(room_id=obj)
        return [p.name.username for p in participants]


class RoomListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            'id',
            'name',
            'count_participants',
            'genres',
            'year_start',
            'year_end',
            'adult',
            'vote_average',
            'is_playing',
            'select_movie'
        )


class RoomWriteSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Room
        fields = (
            'id',
            'name',
            'count_participants',
            'participants',
            'genres',
            'year_start',
            'year_end',
            'adult',
            'vote_average',
            'is_playing',
            'select_movie'
        )


class ParticipantSerializer(serializers.ModelSerializer):
    name = UserSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = (
            'id',
            'name',
            'room_id'
        )


class SwipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swipe
        fields = (
            'id',
            'room',
            'movie',
            'status',
            'participant'
        )
