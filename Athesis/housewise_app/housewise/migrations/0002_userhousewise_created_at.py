# Generated by Django 5.1.1 on 2024-10-02 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housewise', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userhousewise',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
