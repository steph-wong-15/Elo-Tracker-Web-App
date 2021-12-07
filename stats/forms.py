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
        fields = ['match_date','participant_A','score_A', 'participant_B', 'score_B']
        widgets = {
            'match_date': DateInput(),
        }

class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name','admins',]

class AddUpcomingForm(forms.ModelForm):
    class Meta:
        model = Upcoming
        fields = ['participant_A', 'participant_B', 'game', 'date', 'start_time','end_time']
        widgets = {
            'date': DateInput(),
            'start_time': TimeInput(),
            'end_time': TimeInput()
        }




