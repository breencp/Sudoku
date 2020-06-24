# file: views.py
# author: Christopher Breen
# date:
import json
import re
import time

from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .gamerecords import read_file, get_game, save_game
from .leaderboard import calculate_leaders


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
        # test code: replace new_board = and solution = with new_board, solution = for production
        # new_board = custom_board('???2?3??5?5?17??687?2?6??????????8?7???7??93??7?81??4???8?47??35?73???8??396????4')
        # solution = custom_board('')
        new_board, solution = get_game(difficulty)

        request.session['orig_board'] = new_board
        request.session['board'] = new_board
        request.session['solution'] = solution
        request.session['start_time'] = round(time.time())
        if 'end_time' in request.session:
            del request.session['end_time']
        # W = Win, I = In-Progress, L = Lost, S = Surrendered
        request.session['status'] = 'I'
        request.session['hints'] = 0
        return HttpResponseRedirect(reverse('sudoku:play'))


def sanitized_diff(diff):
    if 0 < int(diff) < 3:  # set upper bound to difficulty level not yet ready
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
    diff1_record = calculate_leaders(1)
    diff2_record = calculate_leaders(2)
    diff3_record = calculate_leaders(3)
    diff4_record = calculate_leaders(4)
    diff5_record = calculate_leaders(5)
    return render(request, 'sudoku/leaderboard.html',
                  {'diff1_record': diff1_record,
                   'diff2_record': diff2_record,
                   'diff3_record': diff3_record,
                   'diff4_record': diff4_record,
                   'diff5_record': diff5_record})


def play(request):
    player = request.session.get('player')
    return render(request, 'sudoku/play.html', {'player': player})


def about(request):
    return render(request, 'sudoku/about.html')


def update_board(request):
    end_time = False

    # get JavaScript sessionStorage from POST
    updated_board = json.loads(request.POST.get('board'))
    if corrupted_board(updated_board):
        print('corrupt board')
        # user may have tampered with JavaScript Session Data
        return HttpResponse(status=400)

    start_time = json.loads(request.POST.get('start_time'))
    if not isinstance(start_time, int):
        print('corrupt start time')
        return HttpResponse(status=400)

    status = request.POST.get('status')
    if status not in ['W', 'L', 'I', 'S']:
        print('corrupt status')
        return HttpResponse(status=400)

    try:
        hints = int(request.POST.get('hints'))
    except ValueError:
        return HttpResponse(status=400)

    if status == "W" and request.session['status'] != "W":
        # wasn't won before but it is now
        end_time = round(time.time())
        request.session['end_time'] = end_time
    elif status == "W" and request.session['status'] == "W":
        # already won, don't update end time
        end_time = request.session['end_time']

    # update Django Session
    request.session['board'] = updated_board
    request.session['start_time'] = start_time
    request.session['status'] = status
    request.session['hints'] = hints

    # update SQL3 Database: W = Win, I = In-Progress, L = Lost, S = Surrendered
    data = {'user': request.session['player'],
            'start_time': request.session['start_time'],
            'orig_board': request.session['orig_board'],
            'current_board': request.session['board'],
            'status': request.session['status'],
            'hints': request.session['hints']
            }
    if end_time:
        data.update({'end_time': end_time})

    save_game(data)
    return HttpResponse(status=204)


def corrupted_board(user_board):
    # ensure user_board hasn't been tampered with
    try:
        if len(user_board) != 9:
            raise ValueError
        for row in user_board:
            if len(row) != 9:
                raise ValueError
            for col in row:
                if isinstance(col, list):
                    if not 0 < len(col) < 10:
                        raise ValueError
                    for candidates in col:
                        if not isinstance(candidates, int):
                            raise ValueError
                        elif not 0 < candidates < 10:
                            raise ValueError
                elif not isinstance(col, int):
                    raise ValueError
                elif not 0 < col < 10:
                    raise ValueError
    except:
        return True


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
