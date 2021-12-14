from .models import Upcoming
import django_filters
from django import forms

class UpcomingFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Upcoming
        fields = ['game', 'date']
