from importlib.metadata import requires
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import GuessForm
from .models import TodaysAnswer
from .models import Game
from .wordlists import all_words

# Create your views here.
def index(request):
    return HttpResponse("Hello World!")
"""
def guess(request):
    if request.method == 'POST':
        form = GuessForm(request.POST)
        # TODO: Figure out this section
        g = Game()
        current_guess = form.cleaned_data['guesses'][-1]
        flags = g.evaluate_guess(current_guess)
        g.next_guess(current_guess)
        suggestions = g.show_possible_words()
        context = {'g': g,
        'suggestions': suggestions}
        # TODO: figure out section above
        if form.is_valid():
            return HttpResponseRedirect('/guess/guess')
    else:
        form = GuessForm()
    # form response needs to be passed in as context?
    return render(request, 'guess/guess.html', {'form': form})
"""

class Guess(CreateView):
    model = Game
    template_name = "guess/guess.html"
    fields = ['guess']
#    def form_valid(self, form):
#        guess = self.request.guess
#        valid_guess = guess in all_words
#        if valid_guess: # figure this out...
#            super().form_valid(form)
#        else:
#            super().form_valid(form)

def cheat(request):
    ans = TodaysAnswer().word
    return HttpResponse(f"Today's correct word is: {ans}")