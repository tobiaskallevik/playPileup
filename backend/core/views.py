from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Game
from .serializers import GameSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import time


# Get method for retrieving a list of games from the database.
# The method takes optional query params to give control over the games that are returned.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def games_list(request):
    start_time = time.time()  # Start time for performance measurement

    # Limit and range filtering
    limit = request.query_params.get('limit', 10)  # Takes the limit parameter from the query string. Default is 10.
    start = request.query_params.get('start', 0)  # Start index, default is 0
    end = request.query_params.get('end', None)  # End index, default is None

    # Attribute filtering
    def str_to_int_list(param):
        if param is not None:
            return [int(p) for p in param.split(',')]
        return None

    genres = str_to_int_list(request.query_params.get('genres', None))
    modes = str_to_int_list(request.query_params.get('modes', None))
    themes = str_to_int_list(request.query_params.get('themes', None))
    engines = str_to_int_list(request.query_params.get('engines', None))

    # Tries to convert request parameters
    try:
        limit = int(limit)
        start = int(start)
        end = int(end) if end is not None else None
    except ValueError:
        return Response({'response': 'Invalid limit parameter'}, status=status.HTTP_400_BAD_REQUEST)

    # Checks if the range is valid
    if end is not None and (start < 0 or end <= start):
        return Response({'response': 'Invalid range'}, status=status.HTTP_400_BAD_REQUEST)

    # Query filtering
    query = Q()
    if genres:
        query &= Q(genres__in=genres)
    if modes:
        query &= Q(modes__in=modes)
    if themes:
        query &= Q(themes__in=themes)
    if engines:
        query &= Q(engines__in=engines)

    games = Game.objects.filter(query).distinct()[start:end][:limit]

    # Returns the games as JSON response
    if request.method == 'GET':
        serializer = GameSerializer(games, many=True)
        end_time = time.time()  # End timing
        duration = end_time - start_time
        print(f"games_list executed in {duration} seconds")
        return Response(serializer.data)

    return Response({'response': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


# Method for searching games by name.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_games(request):
    query = request.query_params.get('query', None)

    if query is None:
        return Response({'response': 'No query parameter provided'}, status=status.HTTP_400_BAD_REQUEST)

    games = Game.objects.filter(name__icontains=query)[:10]

    if request.method == 'GET':
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    return Response({'response': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
