# Generated by Django 4.2.11 on 2024-04-24 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='content',
            field=models.TextField(default='Testing'),
        ),
        migrations.AddField(
            model_name='about',
            name='title',
            field=models.CharField(default='testing', max_length=200),
        ),
        migrations.AddField(
            model_name='about',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
