from django.db import models
from django.db.models import Index
from django.conf import settings


class Game(models.Model):
    name = models.CharField(max_length=255)  # The name of the game
    slug = models.CharField(max_length=255)  # The slug of the game
    first_release_date = models.BigIntegerField(null=True)  # The date the game was first released
    rating = models.FloatField(null=True)  # The rating of the game
    rating_count = models.IntegerField(null=True)  # The number of ratings the game has received
    cover_url_low = models.CharField(max_length=255, null=True)  # The URL of the cover image (low resolution)
    cover_url_high = models.CharField(max_length=255, null=True)  # The URL of the cover image (high resolution)
    summary = models.TextField(null=True)  # A summary of the game
    genres = models.ManyToManyField('Genre', related_name='games_genres')
    modes = models.ManyToManyField('Mode', related_name='games_modes')
    themes = models.ManyToManyField('Theme', related_name='games_themes')
    engines = models.ManyToManyField('Engine', related_name='games_engines')

    class Meta:
        verbose_name_plural = "Games"
        indexes = [
            Index(fields=['name'], name='game_name_idx'),
        ]

    def __str__(self):
        return self.name


class UserGame(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    gotten_from = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user} - {self.game}"


# Base model for genres, modes, themes, and engines
class BaseModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Genre(BaseModel):
    class Meta:
        verbose_name_plural = "Genres"
        verbose_name = "Genre"

    pass


class Mode(BaseModel):
    class Meta:
        verbose_name_plural = "Modes"
        verbose_name = "Mode"

    pass


class Theme(BaseModel):
    class Meta:
        verbose_name_plural = "Themes"
        verbose_name = "Theme"

    pass


class Engine(BaseModel):
    class Meta:
        verbose_name_plural = "Engines"
        verbose_name = "Engine"
        indexes = [
            Index(fields=['name'], name='engine_name_idx'),
        ]

    pass





