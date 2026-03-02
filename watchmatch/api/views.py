import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response

from movies.models import Movie
from .serializers import MovieSerializer


@api_view(['GET'])
def detail_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)
