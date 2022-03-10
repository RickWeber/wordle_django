from django.db import models
import datetime
from .wordlists import correct_words, possible_words, all_words

# Create your models here.
class TodaysAnswer(models.Model):
    word = models.CharField(max_length=5)
    day = models.IntegerField(default=0)
    def __init__(self):
        today = datetime.date.today()
        start = datetime.date(2021, 6, 19)
        days_since_start = today - start
        self.day = days_since_start.days
        self.word = correct_words[days_since_start.days]
    def __str__(self):
        return self.word

class Guesses(models.Model):
    pass