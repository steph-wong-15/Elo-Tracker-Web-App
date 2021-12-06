from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='stats-home'),
    path('home/<slug:gameType>/', views.homeUpdate, name='stats-home-update'),
    path('about/', views.about, name='stats-about'),
    path('newgame/', views.newgame, name='stats-newgame'),
    path('game/<slug:slug>/', views.GameDetailView.as_view(), name='stats-game'),
    path('addresults/', views.addresults, name='stats-results'),

]