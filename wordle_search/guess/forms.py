from django import forms
from .models import Game
from .wordlists import all_words

#class GuessForm(forms.Form):
#    guess = forms.CharField(label='Your guess', max_length=5, min_length=5)

class GuessForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = "__all__"
        exclude = ["correct_word"]
        #fields = ["current_guess"]