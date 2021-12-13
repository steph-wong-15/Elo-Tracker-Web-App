from django.contrib import admin
from .models import Company, Game, Results, Match, EloRating, Upcoming
from django.contrib.admin import DateFieldListFilter

class StatsEloRating(admin.ModelAdmin):
    list_display = ('player','game','mu', 'sigma')
    list_filter = ('game',)

class StatsGame(admin.ModelAdmin):
    list_display = ('title','company','slug')
    list_filter = ('company',)

class StatsMatch(admin.ModelAdmin):
    list_display = ('match_title','player_A','player_B','score_A','score_B','elo_A','elo_B','game','match_date')
    list_filter = ('game',('match_date',DateFieldListFilter))

class StatsResult(admin.ModelAdmin):
    list_display = ('result','date_posted')
    list_filter = (('date_posted',DateFieldListFilter),)

class StatsUpcoming(admin.ModelAdmin):
    list_display = ('match_title','game','player_1','player_2','date')
    list_filter = ('game',('date',DateFieldListFilter),)

admin.site.register(Company) 
admin.site.register(Game,StatsGame) 
admin.site.register(Results,StatsResult) 
admin.site.register(Match,StatsMatch) 
admin.site.register(EloRating,StatsEloRating) 
admin.site.register(Upcoming,StatsUpcoming)