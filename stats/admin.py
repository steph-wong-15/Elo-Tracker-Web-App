from django.contrib import admin
from .models import Company, Game, Results, Match, Player, EloRating

admin.site.register(Company)
admin.site.register(Game)
admin.site.register(Results)
admin.site.register(Match)
admin.site.register(Player)
admin.site.register(EloRating)