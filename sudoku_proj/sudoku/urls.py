# Written by Christopher Breen for Sprint 1, last updated June 23, 2020
from django.urls import path

from . import views

app_name = 'sudoku'
urlpatterns = [
    path('', views.index, name='index'),
    path('howtoplay/', views.how_to_play, name='how_to_play'),
    path('newgame/', views.new_game, name='new_game'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('play/', views.play, name='play'),
    path('makegame/', views.make_game, name='make_game'),
    path('update_board/', views.update_board, name='update_board'),
    path('upload/', views.upload, name='upload'),
    path('uploadsuccess/', views.upload_success, name='upload_success')
]
