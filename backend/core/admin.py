from django.contrib import admin

from .models import Game, UserGame, Genre, Mode, Theme, Engine

from django.contrib import admin
from .models import Game, Engine


class GameAdmin(admin.ModelAdmin):
    search_fields = ['name']


class EngineAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Game, GameAdmin)
admin.site.register(Engine, EngineAdmin)
admin.site.register(Genre)
admin.site.register(Mode)
admin.site.register(Theme)
