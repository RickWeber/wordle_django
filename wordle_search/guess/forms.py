from django import forms
from .models import Guesses, TodaysAnswer
from .wordlists import all_words

#class GuessForm(forms.Form):
#    guess = forms.CharField(label='Your guess', max_length=5, min_length=5)

class GuessForm(forms.ModelForm):
    class Meta:
        model = Guesses
        fields = "__all__"
        exclude = ["correct_word"]
        #fields = ["current_guess"]


#class GuessForm(forms.ModelForm):
#    class Meta:
#        model = Guesses
#    pass
#
## This should provide a text input
## The form should validate the entry to make sure it's part 
## of all_words.
## Then it should run Guesses.next_guess() on the input, and
## update the page to show that guess along with the associated
## flags.
#
#
#class CheatForm(forms.ModelForm):
#    class Meta:
#        model = TodaysAnswer