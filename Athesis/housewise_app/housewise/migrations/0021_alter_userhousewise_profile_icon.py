# Generated by Django 5.1.1 on 2024-12-09 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housewise', '0020_rename_likes_project_likes_count_projectlike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhousewise',
            name='profile_icon',
            field=models.CharField(blank=True, default=27, max_length=255, null=True),
        ),
    ]
