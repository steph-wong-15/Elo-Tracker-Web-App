from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import GameRegisterForm,AddResultsForm,CreateCompanyForm, companyInviteForm
from .models import Company, Game,Match
from users.models import User
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

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
    if request.method == 'POST':
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
        users = User.objects.all().filter(company = company)
        form = companyInviteForm()
        return render(request, 'stats/company.html',{'company': company,'users':users,'form':form})

def createCompany(request):
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            company.invite_code = get_random_string(length=32)
            company.save()
            request.user.profile.company=company
            request.user.save()
            messages.success(request, f'Your company has been created!')
            return redirect('stats-home')
    else:
        form = CreateCompanyForm()
    return render(request, 'stats/createCompany.html', {'form': form})

