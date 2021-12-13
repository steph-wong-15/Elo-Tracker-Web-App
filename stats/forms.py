from django import forms
from django.forms import fields
from .models import Company, Game, Match, Upcoming
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

class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']

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
