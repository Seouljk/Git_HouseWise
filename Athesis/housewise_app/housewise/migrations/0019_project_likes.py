# Generated by Django 5.1.1 on 2024-12-06 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housewise', '0018_remove_project_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
