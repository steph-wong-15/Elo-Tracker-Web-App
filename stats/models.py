from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
from django.utils.text import slugify

class Company(models.Model):
    name = models.CharField(max_length=100)
    admins = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f'{self.name}'

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
    player_A = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participant_A', null = True)
    player_B = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participant_B', null = True)
    score_A = models.IntegerField(null = True)
    score_B = models.IntegerField(null = True)
    elo_change = models.IntegerField(null = True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null = True)
    match_date = models.DateField(default = date.today)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.game, allow_unicode=True)
        return super(Match, self).save(*args, **kwargs)

class EloRating(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null = True)
    mu = models.FloatField(null = True)
    sigma = models.FloatField(null = True)

class Results(models.Model):
    date_posted = models.DateTimeField(default=timezone.now)
    score = models.BooleanField
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null = True)

class Upcoming(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null = True)
    date = models.DateField(default = date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()
    player_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_1', null = True)
    player_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_2', null = True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('stats-upcoming', kwargs={'pk': self.pk})

    

    






