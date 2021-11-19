from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

class Company(models.Model):
    name = models.CharField(max_length=100)

class Game(models.Model):
    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, null=True)
    image = models.ImageField(default='game_default.png', upload_to='game_pics')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super(Game, self).save(*args, **kwargs)

class Match(models.Model):
    pass

class Results(models.Model):
    date_posted = models.DateTimeField(default=timezone.now)
    score = models.BooleanField
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null = True)

# class GamePlayer(models.Model):
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
#     match = models.ForeignKey(Match, on_delete=models.CASCADE)
#     player = models.ForeignKey(User, on_delete=models.CASCADE)

    

    






