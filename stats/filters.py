from .models import Upcoming
import django_filters

class UpcomingFilter(django_filters.FilterSet):
    class Meta:
        model = Upcoming
        fields = ['game', 'date']
