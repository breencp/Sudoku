from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .create_game import *


def index(request):
    return render(request, 'sudoku/index.html')


def how_to_play(request):
    return render(request, 'sudoku/howtoplay.html')


def new_game(request):
    return render(request, 'sudoku/newgame.html')


def make_game(request):
    try:
        difficulty = request.POST['difficulty']
        player = request.POST['player_name']
        if player == "":
            request.session['player'] = 'Anonymous'
        else:
            request.session['player'] = player
    except KeyError:
        return render(request, 'sudoku/newgame.html', {
            'error_message': 'Please select a difficulty level.'
        })
    else:
        new_board = create_game(difficulty)
        request.session['board'] = new_board
        return HttpResponseRedirect(reverse('sudoku:play'))


def leaderboard(request):
    return render(request, 'sudoku/leaderboard.html')


def play(request):
    player = request.session.get('player')
    return render(request, 'sudoku/play.html', {'player': player})

