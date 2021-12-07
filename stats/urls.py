from django.urls import path
from . import views
from stats.views import UpcomingList

urlpatterns = [
    path('', views.home, name='stats-home'),
    path('home/<slug:gameType>/', views.homeUpdate, name='stats-home-update'),
    path('about/', views.about, name='stats-about'),
    path('newgame/', views.newgame, name='stats-newgame'),
    path('game/<slug:slug>/', views.GameDetailView.as_view(), name='stats-game'),
    path('results/', views.results, name='stats-results'),
    path('createCompany/', views.createCompany, name='stats-createCompany'),
    path('company/', views.company, name='stats-company'),
    path('schedule/', views.UpcomingList.as_view(), name='stats-schedule'),
    path('newmatch/', views.newmatch, name='stats-newmatch'),

]