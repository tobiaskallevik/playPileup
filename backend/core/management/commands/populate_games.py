from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models
import json


class Command(BaseCommand):
    help = 'Populates the database with data from JSON files'

    @staticmethod
    def get_through_model(app_label, model_name, field_name):
        model = apps.get_model(app_label, model_name)
        field = model._meta.get_field(field_name)
        return field.remote_field.through

    def handle(self, *args, **options):

        self.populate_model_from_json('Game', 'init/games.json', {
            'id': 'id',
            'name': 'name',
            'first_release_date': 'first_release_date',
            'rating': 'rating',
            'rating_count': 'rating_count',
            'slug': 'slug',
            'summary': 'summary',
            'cover_url_low': 'cover_url_low',
            'cover_url_high': 'cover_url_high',
        })
        self.populate_model_from_json('Engine', 'init/engines.json', {
            'id': 'id',
            'name': 'name',
            'slug': 'slug',
        })
        self.populate_model_from_json('Genre', 'init/genres.json', {
            'id': 'id',
            'name': 'name',
            'slug': 'slug',
        })
        self.populate_model_from_json('Mode', 'init/modes.json', {
            'id': 'id',
            'name': 'name',
            'slug': 'slug',
        })
        self.populate_model_from_json('Theme', 'init/themes.json', {
            'id': 'id',
            'name': 'name',
            'slug': 'slug',
        })
        self.populate_model_from_json('core.Game.genres.through', 'init/game_genres.json', {
            'game_id': 'game_id',
            'genre_id': 'genre_id',
        })
        self.populate_model_from_json('core.Game.modes.through', 'init/game_modes.json', {
            'game_id': 'game_id',
            'mode_id': 'mode_id',
        })
        self.populate_model_from_json('core.Game.themes.through', 'init/game_themes.json', {
            'game_id': 'game_id',
            'theme_id': 'theme_id',
        })
        self.populate_model_from_json('core.Game.engines.through', 'init/game_engines.json', {
            'game_id': 'game_id',
            'engine_id': 'engine_id',
        })

    def populate_model_from_json(self, model_name, json_file_path, field_mapping):
        # Check if the model_name indicates a through model and split appropriately
        if 'through' in model_name:
            app_label, model_name, field_name, none = model_name.split('.')
            # Correctly fetch the through model using the get_through_model method
            model = self.get_through_model(app_label, model_name, field_name)
        else:
            # For regular models, continue using apps.get_model
            model = apps.get_model('core', model_name)

        created_count = 0
        updated_count = 0
        count = 0

        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for item in data:
            # Pre-process the data to replace "N/A" with None for numeric fields
            for key in item.keys():
                if item[key] == 'N/A':
                    item[key] = None

            # Construct the defaults dictionary excluding the 'id' field
            defaults = {model_field: item[json_field] for model_field, json_field in field_mapping.items() if
                        model_field != 'id'}

            # Use the 'id' field from the item for lookup in update_or_create
            obj, created = model.objects.update_or_create(
                id=item.get('id'),  # Use the 'id' field for lookup
                defaults=defaults
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

            count += 1

            if count % 1000 == 0:
                self.stdout.write(f'Processed {count} records')

        self.stdout.write(f'Finished processing {model_name}: {created_count} created, {updated_count} updated')

