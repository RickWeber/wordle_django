from django.db import models
import datetime
import random
import re
from typing import NewType
from .wordlists import correct_words, all_words

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
    wordlist = all_words
    guesses = models.CharField(max_length=30)
    correct_word = models.CharField(max_length=5)

    def __init__(self, correct_word = None):
        self.correct_word = correct_word or TodaysAnswer().word
        self.guesses = ""
        self.guesses_taken = 0

    def next_guess(self, guess):
        guess = guess.lower()
        self.guesses_taken += 1
        if self.guesses_taken > 6:
            return "You're out of guesses!"
        self.guesses += guess
        flags = self.evaluate_guess(guess)
        if min(flags) == 2:
            return f"You won! The correct word was {guess}!"
        self.filter_wordlist(guess)

    def evaluate_guess(self, guess):
        correct_letters = list(self.correct_word)
        flags = [2 if c == correct_letters[i] else 0 for i, c in enumerate(guess)]
        letters_to_figure_out = [c for i, c in enumerate(correct_letters) if flags[i] != 2]
        for i, c in enumerate(guess):
            if c in letters_to_figure_out and flags[i] != 2:
                flags[i] = 1
                index_to_remove = letters_to_figure_out.index(c)
                letters_to_figure_out = letters_to_figure_out[:index_to_remove] + letters_to_figure_out[index_to_remove+1:]
        return flags

    def filter_wordlist(self, guess):
        # handy lambda to apply a regex filter
        reg_filter = lambda regex: [w for w in self.wordlist if re.search(regex, w)]
        flags = self.evaluate_guess(guess)
        # filter for letters in the right place (green flags)
        right_position = re.compile("".join(c if f == 2 else '.' for c, f in zip(guess, flags)))
        self.wordlist = reg_filter(right_position)
        # filter for yellow flags
        # first: wrong positions
        wrong_position = re.compile("".join(f"[^{c}]" if flags[i] == 1 else "." for i, c in enumerate(guess)))
        self.wordlist = reg_filter(wrong_position)
        # then words that include at least one of each of the correct letters
        correct_letters = [c for i, c in enumerate(guess) if flags[i] == 1]
        for l in correct_letters:
            has_letter = re.compile(f"[{l}]+")
            self.wordlist = reg_filter(has_letter)
        # finally, filter for known incorrect letters
        drop = "".join([c for c in guess if c not in self.correct_word])
        if drop != "":
            wrong_letters = re.compile(f"[^{drop}]")
            self.wordlist = reg_filter(wrong_letters)

    def show_possible_words(self, n=10):
        if n > len(self.wordlist):
            return random.choices(self.wordlist) # randomize to avoid accidentally giving a hint due to the order of all_words
        return random.choices(self.wordlist, k = n)