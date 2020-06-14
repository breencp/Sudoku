# file: views.py
# author: Christopher Breen
# date:
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .gamerecords import read_file, get_game
import re
import json


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
        # test code, replace new_board = and solution = with new_board, solution = for production
        # new_board = custom_board('???2?3??5?5?17??687?2?6??????????8?7???7??93??7?81??4???8?47??35?73???8??396????4')
        # solution = custom_board('')
        new_board, solution = get_game(difficulty)

        request.session['board'] = new_board
        request.session['solution'] = solution
        return HttpResponseRedirect(reverse('sudoku:play'))


def sanitized_diff(diff):
    if 0 < int(diff) < 3:  # increase 2 as more difficulty levels are programmed
        return str(diff)
    else:
        return False


def sanitized_player(player):
    regex = r"^[\w ]{4,20}$"
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
    # update Django Session
    request.session['board'] = updated_board

    # update SQL3 Database
    # TODO: pass Played.* to function within gamerecords.py for storage in database

    return HttpResponse(status=204)


def upload_success(request):
    return render(request, 'sudoku/uploadsuccess.html')


class UploadFileForm(forms.Form):
    puzzle_file = forms.FileField()


@staff_member_required
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            read_file(request.FILES['puzzle_file'])
            return HttpResponseRedirect(reverse('sudoku:upload_success'))
    else:
        form = UploadFileForm()
        return render(request, 'sudoku/upload.html', {'form': form})
