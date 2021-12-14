from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import GameRegisterForm,AddResultsForm,CreateCompanyForm, companyInviteForm
from .models import Company, Game,Match
from django.utils.timezone import get_default_timezone_name
from .forms import GameRegisterForm,AddResultsForm,CreateCompanyForm, AddUpcomingForm,PromoteAdminForm
from .models import Company, Game, Match, Upcoming, EloRating
from users.models import User, Profile
from django.views.generic.detail import DetailView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from itertools import islice
from datetime import date, datetime
from django.utils.crypto import get_random_string
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from stats.filters import UpcomingFilter
from trueskill import Rating, rate_1vs1, expose, setup

def home(request):
    return redirect('stats-home-refresh', slug='default')

def homeRefresh(request, slug):
    if (request.user.is_authenticated):
        if(not request.user.profile.company):
            return redirect('stats-company')
        context = {}
        user_profile = Profile.objects.filter(user = request.user).first()
        Games = Game.objects.filter(company = user_profile.company)
        if (not Games.exists()):
            return render(request, 'stats/home.html')
        context['Games'] = Games
        Leaders = []
        Recent_Matches = []
        Upcoming_Matches = []
        game = []
        if (slug == 'default'):
            game = Games.first()
        else:
            if (Games.filter(slug = slug).exists()):
                game = Games.filter(company=user_profile.company, slug = slug).first()
        if (isinstance(game,Game)):
            top_ratings = list(EloRating.objects.filter(game = game.id).order_by('-mu')[:3].values_list('player', flat=True))
            for player in top_ratings:
                Leaders.append(User.objects.get(id=player))
            Recent_Matches = Match.objects.filter(game = game.id, match_date__lte=date.today()).order_by('-match_date')[:3]
            Recent_Players = []
            for match in Recent_Matches:
                Recent_Players.append([match.player_A.username,match.player_B.username])
            Upcoming_Matches = Upcoming.objects.filter(game = game.id, date__gte=date.today()).order_by('date')[:3]
            context['Leaders'] = Leaders
            context['Histories'] = Recent_Matches
            context['Upcomings'] = Upcoming_Matches
            context['game_title'] = game.title
        return render(request, 'stats/home.html', context)
    else:
        return render(request, 'stats/home.html')

def about(request):
    return render(request, 'stats/about.html')

def newgame(request):
    if request.method == 'POST':
        form = GameRegisterForm(request.POST)
        if form.is_valid():
            form.instance.company = request.user.profile.company
            form.save()
            messages.success(request, f'Your game has been created!')
            return redirect('stats-home')
    else:
        if( request.user.is_authenticated):
            if(not request.user.profile.company):
                return redirect('stats-company')
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
        form = AddResultsForm(request.POST, game=game)

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
        form = AddResultsForm(game=game)
    return render(request, 'stats/results.html',{'form': form})

class ResultsDetailView(DetailView, LoginRequiredMixin):
    context_object_name = 'results_detail'
    template_name = 'stats/results.html' 
    model = Match
    slug_url_kwarg = 'slug'

@login_required
def company(request):
    if request.method == 'POST':
        if 'promoteUser' in request.POST:
            form = PromoteAdminForm(request.user.profile.company,request.POST)
            if form.is_valid():
                user=form.cleaned_data.get('chosenUser')
                request.user.profile.company.admins.add(user.user)
            return HttpResponseRedirect(request.path_info)
        else:
            form = companyInviteForm(request.POST)
            if form.is_valid():
                inviteCode=form.cleaned_data.get('inviteCode')
                companyQuery = Company.objects.filter(invite_code=inviteCode)
                if companyQuery:
                    request.user.profile.company=companyQuery.get()
                    request.user.profile.save()
                    messages.info(request,f'Successully registered with company '+ companyQuery.get().name)
                    return HttpResponseRedirect(request.path_info)
                else: 
                    messages.error(request,f'Invite code not valid')
            return render(request, 'stats/company.html',{'form':form})
    else:
        company = request.user.profile.company
        admins=[]
        if company:
            admins=company.admins.all()
        isAdmin = request.user in admins
        users = Profile.objects.all().filter(company=company)
        form = companyInviteForm()
        adminForm=None
        if(isAdmin):
            adminForm = PromoteAdminForm(company=company)
        return render(request, 'stats/company.html',{'company': company,'admins':admins,'users':users,'form':form,'adminForm':adminForm,'isAdmin':isAdmin})

def createCompany(request):
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            company.invite_code = get_random_string(length=32)
            company.save()
            company.admins.add(request.user)
            request.user.profile.company=company
            request.user.save()
            messages.success(request, f'Your company has been created!')
            return redirect('stats-home')
    else:
        form = CreateCompanyForm()
    return render(request, 'stats/createCompany.html', {'form': form})

def schedule(request):
    if( request.user.is_authenticated):
        if(not request.user.profile.company):
            return redirect('stats-company')
    return render(request, 'stats/schedule.html')

def newmatch(request):
    company = request.user.profile.company
    if request.method == 'POST':
        form = AddUpcomingForm(request.POST, company=company)

        if form.is_valid():
            upcoming = form.cleaned_data
            subject = "Upcoming Match"
            message = "Hello, here is a friendly reminder you have an upcoming match scheduled!"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [upcoming['player_1'].email, upcoming['player_2'].email])
            form.save()
            messages.success(request, f'A match has been scheduled & participants will be notified through email!')

            return redirect('stats-schedule')
    else:
        form = AddUpcomingForm(company=company)
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
                
    ratings.append(round(currentRating))

    ratings = list(reversed(ratings))

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
        recentsize = 3

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
        context['Game'] = self.get_object()

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
            raise Http404("Rating does not exist")
            return {}
        #find the users position on the ladder
        position = list(EloRating.objects.filter(game = self.get_object())).index(user) + 1

        #Find all matches in which user was a player
        matches = Match.objects.filter(Q(player_B = user.player) | Q(player_A = user.player)).order_by('match_date', 'id')

        
        context['position'] = position
        context['rating']  = round(expose(Rating(mu=user.mu, sigma=user.sigma)))
        context['username'] = user.player.username

        recentsize = 20
        recentmatches = islice(list(matches), 0, recentsize)
        context['matches'] = recentmatches

        change = []

        prev, wins = previousRatings(context['rating'], user.player, list(matches))
        
        prev = list(reversed(prev))

        if len(matches) > 1:
            for match in matches:
                match.change = prev[list(matches).index(match)+1] - prev[list(matches).index(match)]
                change.append(match.change)

        elif len(matches) == 1:
            change = [context['rating']] 
            #prev = [context['rating']]     
            matches[0].change = context['rating']           
            
        else:
            #prev = [0]
            change = [0]

        context['wins'] = wins[0]
        context['losses'] = wins[1]
        context['draws'] = wins[2]
        context['JSData'] = change

        return context


class UpcomingUpdateView(SuccessMessageMixin, UpdateView):
    model = Upcoming
    template_name = 'stats/updatematch.html'
    form_class = AddUpcomingForm
    success_message = 'Upcoming match successfully updated!'

class UpcomingDeleteView(DeleteView):
    model = Upcoming
    template_name = 'stats/deletematch.html'
    success_url = reverse_lazy('stats-schedule')

def search(request):
    if( request.user.is_authenticated):
        if(not request.user.profile.company):
            return redirect('stats-company')

    today = date.today()
    upcoming_list = Upcoming.objects.filter(date__gte=today)
    upcoming_filter = UpcomingFilter(request.GET, queryset=upcoming_list)
    return render(request, 'stats/schedule.html', {'filter': upcoming_filter})
