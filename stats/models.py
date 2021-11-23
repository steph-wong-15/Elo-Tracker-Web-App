from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

class Company(models.Model):
    name = models.CharField(max_length=100)

class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name =  models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

class Game(models.Model):
    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, null=True)
    image = models.ImageField(default='game_default.png', upload_to='game_pics')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super(Game, self).save(*args, **kwargs)

class Match(models.Model):
    participant_A = models.ForeignKey(Player, on_delete=models.CASCADE)
    participant_B = models.ForeignKey(Player, on_delete=models.CASCADE)

    score_A = models.IntegerField(max_length=10)
    score_B = models.IntegerField(max_length=10)
    elo_change = models.IntegerField(max_length=20)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    match_date = models.DateTimeField(default=timezone.now)

# class Results(models.Model):
#     date_posted = models.DateTimeField(default=timezone.now)
#     score = models.BooleanField
#     match = models.ForeignKey(Match, on_delete=models.CASCADE, null = True)

# class GamePlayer(models.Model):
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
#     match = models.ForeignKey(Match, on_delete=models.CASCADE)
#     player = models.ForeignKey(User, on_delete=models.CASCADE)

    

    






