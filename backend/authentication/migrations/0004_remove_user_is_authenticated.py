# Generated by Django 5.0.6 on 2024-07-28 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0003_remove_profile_bio_remove_profile_full_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_authenticated",
        ),
    ]