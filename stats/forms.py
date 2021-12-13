from django import forms
from django.forms import fields
from .models import Company, Game, Match, Upcoming, EloRating
from django.forms import ModelForm

class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'

class GameRegisterForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'company', 'image']

class AddResultsForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['match_date','player_A','score_A', 'player_B', 'score_B']
        widgets = {
            'match_date': DateInput(),
        }
    def __init__(self, **kwargs):
        game = kwargs.pop('game', None)
        super().__init__(**kwargs)
        
        self.fields['player_A'].queryset = EloRating.objects.filter(game = game)
        self.fields['player_B'].queryset = EloRating.objects.filter(game = game)

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
