from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
import re
import json

from .create_game import *


def index(request):
    return render(request, 'sudoku/index.html')


def how_to_play(request):
    return render(request, 'sudoku/howtoplay.html')


def new_game(request):
    return render(request, 'sudoku/newgame.html')


def make_game(request):
    try:
        difficulty = sanitized_diff(request.POST['difficulty'])
        if not difficulty:
            return render(request, 'sudoku/newgame.html', {
                'error_message': 'Sorry, that difficulty level is not yet available.'
            })

        request.session['player'] = sanitized_player(request.POST['player_name'])
    except KeyError:
        return render(request, 'sudoku/newgame.html', {
            'error_message': 'Please select a difficulty level.'
        })
    else:
        new_board = create_game(difficulty)
        request.session['board'] = new_board
        return HttpResponseRedirect(reverse('sudoku:play'))


def sanitized_diff(diff):
    if 0 < int(diff) < 2:  # increase 2 as more difficulty levels are programmed
        return str(diff)
    else:
        return False


def sanitized_player(player):
    regex = r"^[\w ]{4,16}$"
    match = re.fullmatch(regex, player)
    if match:
        return match[0]
    else:
        return 'Anonymous'


def leaderboard(request):
    return render(request, 'sudoku/leaderboard.html')


def play(request):
    player = request.session.get('player')
    return render(request, 'sudoku/play.html', {'player': player})


def about(request):
    return render(request, 'sudoku/about.html')


def update_board(request):
    updated_board = json.loads(request.POST.get('board'))
    request.session['board'] = updated_board
    return HttpResponse(status=204)

