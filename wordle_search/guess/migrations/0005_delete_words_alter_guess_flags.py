# Generated by Django 4.0.3 on 2022-04-14 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guess', '0004_game_guess_words_delete_guesses_game_guess'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Words',
        ),
        migrations.AlterField(
            model_name='guess',
            name='flags',
            field=models.CharField(default='00000', max_length=5),
        ),
    ]
