# Written by Christopher Breen for Sprint 1, last updated June 29, 2020 for Sprint 2
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
    path('uploadsuccess/', views.upload_success, name='upload_success'),
    path('get_hint/', views.get_hint, name='get_hint'),
    path('erase_obvious/', views.erase_obvious, name='erase_obvious'),
    path('load_puzzle/', views.load_puzzle, name='load_puzzle'),
    path('puzzleload/', views.puzzleload, name='puzzleload'),
    path('customgame/', views.custom_game, name='custom_game'),
    path('loadcustom/', views.load_custom, name='load_custom')
]
