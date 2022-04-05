from importlib.metadata import requires
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import GuessForm
from .models import TodaysAnswer

# Create your views here.
def index(request):
    return HttpResponse("Hello World!")

def guess(request):
    if request.method == 'POST':
        form = GuessForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/guess/guess')
    else:
        form = GuessForm()
    return render(request, 'guess/guess.html', {'form': form})

def cheat(request):
    ans = TodaysAnswer().word
    return HttpResponse(f"Today's correct word is: {ans}")