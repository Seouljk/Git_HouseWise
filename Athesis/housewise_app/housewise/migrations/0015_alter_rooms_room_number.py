# Generated by Django 5.1.1 on 2024-12-06 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housewise', '0014_project_cr_count_project_project_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='room_number',
            field=models.CharField(default=1, max_length=50),
        ),
    ]
