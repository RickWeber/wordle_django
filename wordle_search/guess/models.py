from django.db import models
import datetime
import random
import re
from .wordlists import correct_words, all_words

class TodaysAnswer(models.Model):
    word = models.CharField(max_length=5) # should there be a min length too?
    day = models.IntegerField(default=0)
    def __init__(self):
        today = datetime.date.today()
        start = datetime.date(2021, 6, 18)
        days_since_start = today - start # might have an issue with rounding. Am I off by a day if I check in the morning?
        self.day = days_since_start.days
        self.word = correct_words[days_since_start.days]
    def __str__(self):
        return self.word

class Guesses(models.Model):
    guesses = models.CharField(max_length=30)
    correct_word = models.CharField(max_length=5)

    def __init__(self, correct_word = None):
        self.correct_word = correct_word or TodaysAnswer().word
        self.current_guess = models.CharField(max_length=5)
        self.guesses = []
        self.wordlist = all_words

    def next_guess(self, guess):
        guess = guess.lower()
        self.guesses_taken += 1
        if len(self.guesses) > 6:
            return "You're out of guesses!"
        self.guesses += [guess]
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
        # then words that include at least one of each of the correct letters. 
        # TODO: make sure to filter for at least n of each the correct letters if we know there's at least n copies of that letter.
        correct_letters = [c for i, c in enumerate(guess) if flags[i] == 1]
        for l in correct_letters:
            has_letter = re.compile(f"[{l}]+")
            self.wordlist = reg_filter(has_letter)
        # finally, filter for known incorrect letters
        # Note: we're not actually looking for cases where we get a gray flag on a second letter
        # (e.g. guess = "loose", flags = "02000") just dropping all the letters we know aren't in there.
        drop = "".join([c for c in guess if c not in self.correct_word])
        if drop != "":
            wrong_letters = re.compile(f"[^{drop}]" + "{5}") # don't let it show up anywhere
            self.wordlist = reg_filter(wrong_letters)
        # look at letters that were flagged gray but have another instance in the correct word
        greys_not_dropped = [c for i, c in enumerate(guess) if flags[i] == 0 and c in self.correct_word]
        for g in greys_not_dropped:
            copies_in_word = self.correct_word.count(g)
            extra_letters = re.compile(f"[^{g}]" + "{" + f"{copies_in_word + 1}" + ",}")
            self.wordlist = reg_filter(extra_letters)

    def show_possible_words(self, n=10):
        if n > len(self.wordlist):
            return random.sample(self.wordlist, k = len(self.wordlist))
        return random.sample(self.wordlist, k = n)

class Evaluate_words(models.Model):
    wordlist = all_words
    guesses = models.CharField(max_length=30)
    correct_word = models.CharField(max_length=5)

    def __init__(self, correct_word = None):
        self.correct_word = correct_word or TodaysAnswer().word
        self.guesses = ""
        self.guesses_taken = 0

    def one_guess(self, guess):
        g = Guesses(self.correct_word)
        g.next_guess(guess)
        return len(all_words) - len(g.wordlist)