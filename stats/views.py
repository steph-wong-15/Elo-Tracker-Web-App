from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import get_default_timezone_name
from .forms import GameRegisterForm,AddResultsForm,CreateCompanyForm, AddUpcomingForm
from .models import Company, Game, Match, Player, Upcoming, EloRating
from users.models import User
from django.views.generic.detail import DetailView
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from trueskill import Rating, rate_1vs1, expose, setup

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

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        context['Matches'] = Match.objects.filter(game=self.get_object())
        if EloRating.objects.filter(player=self.request.user.id, game=self.get_object()).exists():
            context['EloRating'] = EloRating.objects.get(player=self.request.user.id, game=self.get_object())
        else:
            context['EloRating'] = None
        return context

def results(request, **kwargs):
    slug = kwargs['slug']
    game = Game.objects.get(slug=slug)

    if request.method == 'POST':
        form = AddResultsForm(request.POST)

        if form.is_valid():
            player_A = EloRating.objects.get(player = form.cleaned_data['player_A'], game = game)
            player_B = EloRating.objects.get(player = form.cleaned_data['player_B'], game = game)

            form.instance.game = game
            form.instance.elo_A = expose(Rating(mu=player_A.mu, sigma=player_A.sigma))
            form.instance.elo_B = expose(Rating(mu=player_B.mu, sigma=player_B.sigma))

            if form.cleaned_data['score_A'] == form.cleaned_data['score_B']:
                newElo_A, newElo_B = rate_1vs1(Rating(mu=player_A.mu, sigma=player_A.sigma), Rating(mu=player_B.mu, sigma=player_B.sigma), drawn=True)
                
            elif form.cleaned_data['score_A'] > form.cleaned_data['score_B']:
                newElo_A, newElo_B = rate_1vs1(Rating(mu=player_A.mu, sigma=player_A.sigma), Rating(mu=player_B.mu, sigma=player_B.sigma))
            else:
                newElo_B, newElo_A = rate_1vs1(Rating(mu=player_B.mu, sigma=player_B.sigma), Rating(mu=player_A.mu, sigma=player_A.sigma))
            
            player_A.mu, player_A.sigma = newElo_A
            player_B.mu, player_B.sigma = newElo_B
            player_A.save()
            player_B.save()

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

def schedule(request):
    return render(request, 'stats/schedule.html')

def newmatch(request):
    if request.method == 'POST':
        form = AddUpcomingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your match has been scheduled!')
            return redirect('stats-schedule')
    else:
        form = AddUpcomingForm()
    return render(request, 'stats/newmatch.html', {'form': form})

class UpcomingList(ListView,LoginRequiredMixin):
    model = Upcoming
    template_name = 'stats/schedule.html'
    context_object_name = 'upcomings'
    ordering = ['date','start_time']

class UpcomingDetailView(DetailView,LoginRequiredMixin):
    model = Upcoming
    template_name = 'stats/upcoming.html'

def joinGame(request, **kwargs):
    setup(mu=1000, sigma=333.333, tau=3.33333, beta=166.666)  
    slug = kwargs['slug']
    game = Game.objects.filter(slug=slug)[0]

    if EloRating.objects.filter(player=request.user.id, game=game).exists():
        print('jh')
    else:
        rating = EloRating()
        rating.player = request.user
        rating.game = game
        rating.mu, rating.sigma = Rating(1000)
        rating.save()

    return redirect('stats-home')