# Generated by Django 5.0.6 on 2024-07-19 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='companies',
        ),
        migrations.AddIndex(
            model_name='engine',
            index=models.Index(fields=['name'], name='engine_name_idx'),
        ),
        migrations.AddIndex(
            model_name='game',
            index=models.Index(fields=['name'], name='game_name_idx'),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
