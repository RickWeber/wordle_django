from importlib.metadata import requires
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import GuessForm
from .models import TodaysAnswer
from .models import Guesses

# Create your views here.
def index(request):
    return HttpResponse("Hello World!")

def guess(request):
    if request.method == 'POST':
        form = GuessForm(request.POST)
        # TODO: Figure out this section
        g = Guesses()
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

def cheat(request):
    ans = TodaysAnswer().word
    return HttpResponse(f"Today's correct word is: {ans}")