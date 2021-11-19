from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import GameRegisterForm
from .models import Game
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    Games = Game.objects.all()

    context = {'Games': Games}

    return render(request, 'stats/home.html',context)

def about(request):
    return render(request, 'stats/about.html')

def newgame(request):
    if request.method == 'POST':
        form = GameRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your game has been created!')
            return redirect('stats-home')
    else:
        form = GameRegisterForm()
    return render(request, 'stats/newgame.html', {'form': form})

class GameDetailView(DetailView,LoginRequiredMixin):
    context_object_name = 'game_detail'
    template_name = 'stats/game.html' 
    model = Game
    slug_url_kwarg = 'slug'

#result also needs slug
def results(request):
    return render(request, 'stats/results.html')
