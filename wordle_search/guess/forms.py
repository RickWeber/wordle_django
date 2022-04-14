from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from .models import Game, Guess
from .wordlists import all_words

#class GuessForm(forms.Form):
#    guess = forms.CharField(label='Your guess', max_length=5, min_length=5)

class GuessForm(forms.ModelForm):
    class Meta:
        model = Guess
        fields = ["guess"]
    guess = forms.CharField(validators=[
        validators.MinLengthValidator(5, "Please enter a 5 letter guess."),
        validators.MaxLengthValidator(5, "Please enter a 5 letter guess."),
    ])
    g = Guess(guess)