# Generated by Django 4.2.11 on 2024-04-28 00:25

from django.db import migrations, models
import tasks.models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20240425_0127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='slug',
            field=models.SlugField(default=tasks.models.randomString, max_length=200, unique=True),
        ),
    ]