from django import forms
from django.forms import fields
from .models import Company, Game, Match

class GameRegisterForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'company', 'image']

class AddResultsForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['game', 'match_date','participant_A','score_A', 'participant_B', 'score_B']


class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name','admins',]


