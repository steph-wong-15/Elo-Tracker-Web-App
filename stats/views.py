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
from django.db.models import Q

from itertools import islice
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

#Takes the current rating and a sorted list of matches
#returns a list of previous ratings
def previousRatings(currentRating, player, matchList):
    ratings = []
    ratings.append(round(currentRating))

    wins = 0
    losses = 0
    draws = 0

    for match in matchList:
        if match.player_A == player:
            ratings.append(round(match.elo_A))
            if(match.score_A > match.score_B):
                wins += 1
                match.result = 'W'
            elif(match.score_B > match.score_A):
                losses += 1
                match.result = 'L'
            else:
                draws += 1
                match.result = 'D'
        elif match.player_B == player:
            ratings.append(round(match.elo_B))
            if(match.score_B > match.score_A):
                wins += 1
                match.result = 'W'
            elif(match.score_A > match.score_B):
                losses += 1
                match.result = 'L'
            else:
                draws += 1
                match.result = 'D'
                

    return ratings, [wins, losses, draws]


class LeaderBoardList(DetailView, LoginRequiredMixin):

    model = Game
    context_object_name = 'player_list'
    template_name = 'stats/leaderboard.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(LeaderBoardList, self).get_context_data(**kwargs)
        ratings = EloRating.objects.filter(game=self.get_object())
        
        matches = Match.objects.filter(game=self.get_object())
        recentsize = 1

        for rating in ratings:
            rating.expose = round(expose(Rating(mu=rating.mu, sigma=rating.sigma)))
            rating.url = str(rating.player_id)

            prev, wins = previousRatings(rating.expose, rating.player, matches)
            recentchange = round(rating.expose - prev[min(len(prev)-1, recentsize)])
            rating.recent = recentchange
            rating.wins = wins[0]
            rating.losses = wins[1]
            rating.draws = wins[2]

        ratings = sorted(list(ratings), key=lambda x: x.expose, reverse=True)
        
        for rating in ratings:
            rating.position = ratings.index(rating)+1
        context['Ratings'] = ratings

        context['JSData'] = list(map(lambda x: expose(Rating(mu=x.mu, sigma=x.sigma)), list(ratings)))

        return context



class LeaderBoardRating(DetailView, LoginRequiredMixin):

    model = Game
    context_object_name = 'game'
    template_name = 'stats/leaderboardProfile.html'
    slug_url_kwarg = 'game'
    
    
    
    def get_context_data(self, **kwargs):

        context = super(LeaderBoardRating, self).get_context_data(**kwargs)

        try:
            user = EloRating.objects.filter(game = self.get_object(), player = self.kwargs['rating_id'])[0]
        except IndexError:
            #404, user has no rating for this game or does not exist
            return()

        #find the users position on the ladder
        position = list(EloRating.objects.filter(game = self.get_object())).index(user) + 1

        #Find all matches in which user was a player
        matches = Match.objects.filter(Q(player_B = user.player) | Q(player_A = user.player)).order_by('match_date', '-id')

        
        context['position'] = position
        context['rating']  = round(expose(Rating(mu=user.mu, sigma=user.sigma)))
        context['username'] = user.player.username

        recentsize = 5
        recentmatches = islice(list(matches), 0, recentsize)
        context['matches'] = recentmatches

        prev, wins = previousRatings(context['rating'], user.player, list(matches))
        if len(matches) > 1:
            for match in matches:
                match.change = prev[list(matches).index(match)] - prev[list(matches).index(match)+1]

        elif len(matches) == 1:
            prev = [context['rating']]     
            matches[0].change = context['rating']           

        else:
            prev = [0]
        # recentchange = context['rating'] - prev[min(len(prev)-1, recentsize)]
        # context['recent'] = recentchange

        context['wins'] = wins[0]
        context['losses'] = wins[1]
        context['draws'] = wins[2]
        context['JSData'] = prev

        return context


    