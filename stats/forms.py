from django import forms
from .models import Game
from .models import Match

class GameRegisterForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'company']

class AddResultsForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['match_date','participant_A','score_A', 'participant_B', 'score_B']


    



