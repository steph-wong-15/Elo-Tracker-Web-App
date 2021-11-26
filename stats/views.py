from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import GameRegisterForm,AddResultsForm,CreateCompanyForm
from .models import Company, Game,Match
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

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
    if request.method == 'POST':
        form = AddResultsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your match results were added!')
            return redirect('stats-home')
    else:
        form = AddResultsForm()
    return render(request, 'stats/results.html',{'form': form})

class ResultsDetailView(DetailView, LoginRequiredMixin):
    context_object_name = 'results_detail'
    template_name = 'stats/results.html' 
    model = Match
    slug_url_kwarg = 'slug'


@login_required
def company(request):
    company = request.user.profile.company
    context = {'company': company}

    return render(request, 'stats/company.html',context)

def createCompany(request):
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            request.user.profile.company=company
            request.user.save()
            messages.success(request, f'Your company has been created!')
            return redirect('stats-home')
    else:
        form = CreateCompanyForm()
    return render(request, 'stats/createCompany.html', {'form': form})

