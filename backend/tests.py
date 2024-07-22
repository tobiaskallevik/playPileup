from django.test import TestCase
from core.models import Game, Genre, Mode, Theme, Engine, UserGame
from django.contrib.auth import get_user_model

class ModelsTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Action', slug='action')
        self.mode = Mode.objects.create(name='Single Player', slug='single-player')
        self.theme = Theme.objects.create(name='Adventure', slug='adventure')
        self.engine = Engine.objects.create(name='Unreal Engine', slug='unreal-engine')
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')

    def test_game_creation(self):
        game = Game.objects.create(
            name='Test Game',
            slug='test-game',
            first_release_date=20230101,
            rating=4.5,
            rating_count=100,
            cover_url_low='http://example.com/low.jpg',
            cover_url_high='http://example.com/high.jpg',
            summary='This is a test game.'
        )
        game.genres.add(self.genre)
        game.modes.add(self.mode)
        game.themes.add(self.theme)
        game.engines.add(self.engine)

        self.assertEqual(game.name, 'Test Game')
        self.assertEqual(game.slug, 'test-game')
        self.assertEqual(game.first_release_date, 20230101)
        self.assertEqual(game.rating, 4.5)
        self.assertEqual(game.rating_count, 100)
        self.assertEqual(game.cover_url_low, 'http://example.com/low.jpg')
        self.assertEqual(game.cover_url_high, 'http://example.com/high.jpg')
        self.assertEqual(game.summary, 'This is a test game.')
        self.assertIn(self.genre, game.genres.all())
        self.assertIn(self.mode, game.modes.all())
        self.assertIn(self.theme, game.themes.all())
        self.assertIn(self.engine, game.engines.all())

    def test_user_game_creation(self):
        game = Game.objects.create(name='Test Game', slug='test-game')
        user_game = UserGame.objects.create(user=self.user, game=game, gotten_from='Epic Games Store')

        self.assertEqual(user_game.user, self.user)
        self.assertEqual(user_game.game, game)
        self.assertEqual(user_game.gotten_from, 'Epic Games Store')