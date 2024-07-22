from django.urls import path
from .views import games_list, search_games

urlpatterns = [
    path('games/', games_list, name='game-list'),
    path('search/', search_games, name='search-games'),
]
