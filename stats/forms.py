from django import forms
from django.forms import fields
from .models import Company, Game, Match, Upcoming, EloRating
from users.models import User, Profile
from django.forms import ModelForm

class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'

class GameRegisterForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'image']

class AddResultsForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['match_date','player_A','score_A', 'player_B', 'score_B']
        widgets = {
            'match_date': DateInput(),
        }
    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game', None)
        super().__init__(*args, **kwargs)
        
        self.fields['player_A'].queryset = User.objects.filter(elorating__in=(EloRating.objects.filter(game = game)))
        self.fields['player_B'].queryset = User.objects.filter(elorating__in=(EloRating.objects.filter(game = game)))

class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name','admins',]

class companyInviteForm(forms.Form):
    inviteCode = forms.CharField(label="Invite Code",max_length=32,required=True)

class AddUpcomingForm(forms.ModelForm):
    class Meta:
        model = Upcoming
        fields = ['player_1', 'player_2', 'game', 'date', 'start_time','end_time']
        widgets = {
            'date': DateInput(),
            'start_time': TimeInput(),
            'end_time': TimeInput(),
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        
        self.fields['game'].queryset = Game.objects.filter(company=company)
        self.fields['player_1'].queryset = User.objects.filter(profile__in=(Profile.objects.filter(company=company)))
        self.fields['player_2'].queryset = User.objects.filter(profile__in=(Profile.objects.filter(company=company)))
        
