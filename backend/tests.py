from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.models import Game, Genre, Mode, Theme, Engine
from authentication.models import User  # Import the custom user model


class GamesListAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='tester', password='testPass1.')
        self.client.force_authenticate(user=self.user)

        # Create Genre, Mode, Theme, and Engine instances
        genre1 = Genre.objects.create(name='Genre 1')
        genre2 = Genre.objects.create(name='Genre 2')
        mode1 = Mode.objects.create(name='Mode 1')
        mode2 = Mode.objects.create(name='Mode 2')
        theme1 = Theme.objects.create(name='Theme 1')
        theme2 = Theme.objects.create(name='Theme 2')
        engine1 = Engine.objects.create(name='Engine 1')
        engine2 = Engine.objects.create(name='Engine 2')

        # Create Game instances and assign the Genre, Mode, Theme, and Engine instances
        self.game1 = Game.objects.create(name='Game 1')
        self.game1.genres.set([genre1])
        self.game1.modes.set([mode1])
        self.game1.themes.set([theme1])
        self.game1.engines.set([engine1])

        self.game2 = Game.objects.create(name='Game 2')
        self.game2.genres.set([genre2])
        self.game2.modes.set([mode2])
        self.game2.themes.set([theme2])
        self.game2.engines.set([engine2])

        self.game3 = Game.objects.create(name='Game 3')
        self.game3.genres.set([genre1])
        self.game3.modes.set([mode2])
        self.game3.themes.set([theme1])
        self.game3.engines.set([engine2])

        self.url = reverse('game-list')  # URL to the games list endpoint

    # Test no filter
    def test_get_games_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    # Test limit filter
    def test_get_games_list_with_limit(self):
        response = self.client.get(self.url, {'limit': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # Test invalid limit filter
    def test_get_games_list_with_invalid_limit(self):
        response = self.client.get(self.url, {'limit': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test ganre filter
    def test_get_games_list_with_genre_filter(self):
        response = self.client.get(self.url, {'genres': '1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # Test ganre and mode filter
    def test_get_games_list_with_multiple_filters(self):
        response = self.client.get(self.url, {'genres': '1', 'modes': '2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
