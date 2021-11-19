from django import forms
from .models import Game

class GameRegisterForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'company']


    



