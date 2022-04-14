# Generated by Django 4.0.3 on 2022-04-14 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guess', '0003_evaluate_words'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Guess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guess', models.CharField(max_length=5)),
                ('flags', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.DeleteModel(
            name='Guesses',
        ),
        migrations.AddField(
            model_name='game',
            name='guess',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guess.guess'),
        ),
    ]