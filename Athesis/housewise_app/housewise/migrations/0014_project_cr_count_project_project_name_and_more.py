# Generated by Django 5.1.1 on 2024-12-06 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housewise', '0013_remove_project_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='cr_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='project_name',
            field=models.CharField(default='Unnamed Project', max_length=255),
        ),
        migrations.AddField(
            model_name='project',
            name='room_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rooms',
            name='room_number',
            field=models.CharField(default='Room', max_length=50),
        ),
    ]
