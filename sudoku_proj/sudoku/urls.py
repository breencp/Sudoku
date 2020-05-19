from django.urls import path

from . import views

app_name = 'sudoku'
urlpatterns = [
    path('', views.index, name='index'),
    path('howtoplay/', views.how_to_play, name='how_to_play'),
    path('newgame/', views.new_game, name='new_game'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('sudoku/', views.sudoku, name='sudoku')
]