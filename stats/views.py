from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import GameRegisterForm,AddResultsForm,CreateCompanyForm
from .models import Company, Game,Match
from users.models import User
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def homeUpdate(request, gameType):
    # Games = Game.objects.filter(company=request.user.company.id) #will filter for games within the company
    Games = [
        {
            "title":"Basketball",
            "slug":"basketball",
            "image":{
                "url":'/media/game_default.png'
            },
            "company":{
                "name":"CompanyA"
            }
        },
        {
            "title":"Soccer",
            "slug":"soccer",
            "image":{
                "url":'/media/game_default.png'
            },
            "company":{
                "name":"CompanyA"
            }
        },
        {
            "title":"Tennis",
            "slug":"tennis",
            "image":{
                "url":'/media/game_default.png'
            },
            "company":{
                "name":"CompanyA"
            }
        }
    ]
    Leaders = Player.objects.order_by('id')
    Histories = [
        {"title":"Soccer","match_date":"2021-11-15"},
        {"title":"Tennis","match_date":"2021-11-12"},
        {"title":"Soccer","match_date":"2021-11-11"},
        {"title":"Tennis","match_date":"2021-11-10"},
        {"title":"basketball","match_date":"2021-11-01"},
    ]
    Upcomings = [
        {"title":"basketball","match_date":"2021-12-01"},
        {"title":"basketball","match_date":"2021-12-02"},
        {"title":"Soccer","match_date":"2021-12-03"},
        {"title":"Tennis","match_date":"2021-12-04"},
        {"title":"Tennis","match_date":"2021-12-05"},
    ]
    Leaders = [
            {"first_name":gameType+"1","last_name":"last1"},
            {"first_name":gameType+"2","last_name":"last2"},
            {"first_name":gameType+"3","last_name":"last3"},
    ]     
    context = {'Games': Games, 'Histories': Histories, 'Upcomings':Upcomings, 'Leaders':Leaders, 'GameType':gameType}
    return render(request, 'stats/home.html',context)

def home(request):
    return redirect('stats-home-update', gameType='default')

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
    users = User.objects.all().filter(company = company)
    context = {'company': company,'users':users}

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

