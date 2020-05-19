from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .sudoku_logic import *


def index(request):
    return render(request, 'sudoku/index.html')


def how_to_play(request):
    return render(request, 'sudoku/howtoplay.html')


def new_game(request):
    return render(request, 'sudoku/newgame.html')


def make_game(request):
    try:
        selected_diff = request.POST['difficulty']
        player_name = request.POST['player_name']
    except KeyError:
        return render(request, 'sudoku/newgame.html', {
            'error_message': 'Please enter your name and select a difficulty level.'
        })
    else:
        new_board = create_board()
        return HttpResponseRedirect(reverse('sudoku:play', {'new_board': new_board}))


def leaderboard(request):
    return render(request, 'sudoku/leaderboard.html')


def play(request):
    return render(request, 'sudoku/play.html')
