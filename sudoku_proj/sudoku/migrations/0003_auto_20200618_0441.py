# Generated by Django 3.0.6 on 2020-06-18 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sudoku', '0002_remove_played_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='played',
            name='end_time',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='played',
            name='start_time',
            field=models.IntegerField(null=True),
        ),
    ]
