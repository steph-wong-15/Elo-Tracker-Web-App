from django.urls import path
from . import views
from stats.views import UpcomingList, UpcomingDetailView

urlpatterns = [
    path('', views.home, name='stats-home'),
    path('about/', views.about, name='stats-about'),
    path('newgame/', views.newgame, name='stats-newgame'),
    path('game/<slug:slug>/', views.GameDetailView.as_view(), name='stats-game'),
    path('results/<slug:slug>/', views.results, name='stats-results'),
    path('createCompany/', views.createCompany, name='stats-createCompany'),
    path('company/', views.company, name='stats-company'),
    path('schedule/', views.UpcomingList.as_view(), name='stats-schedule'),
    path('schedule/new/', views.newmatch, name='stats-newmatch'),
    path('schedule/<pk>/', views.UpcomingDetailView.as_view(), name='stats-upcoming'),
    path('joingame/<slug:slug>/', views.joinGame, name='stats-joingame'),
    path('game/<slug:slug>/leaderboard/', views.LeaderBoardList.as_view(), name='stats-leaderboard'),
    path('game/<slug:game>/leaderboard/<int:rating_id>', views.LeaderBoardRating.as_view(), name='stats-leaderboard-rating'),
]