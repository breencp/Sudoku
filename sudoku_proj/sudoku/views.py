# file: views.py
# author: Christopher Breen
# last updated: June 29, 2020
import copy
import json
import re
import time

from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .gamerecords import read_file, get_game, save_game, retrieve_puzzle
from .leaderboard import calculate_leaders
from .techniques import hidden_pair, naked_quad, hidden_triplet
from .techniques import hidden_quad, xwing, swordfish
from .techniques import naked_pair, omission, naked_triplet
from .techniques import naked_single, hidden_single


def index(request):
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
    return render(request, 'sudoku/index.html')


def how_to_play(request):
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
    return render(request, 'sudoku/howtoplay.html')


def new_game(request):
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
    return render(request, 'sudoku/newgame.html')


def puzzleload(request):
    # Written by Ben Brandhorst for Sprint 2, last updated July 4, 2020
    request.session['puzzleID'] = sanitized_puzzleid(request.POST['puzzleID'])
    return render(request, 'sudoku/puzzleload.html', )


def make_game(request):
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
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
        # new_board = json.dumps(custom_board('63214597881??9???4?4??8??1????85????16?274??????96????481529?6?753416??9296738?4?'))
        # solution = json.dumps(custom_board('632145978817692534945387612324851796169274853578963421481529367753416289296738145'))
        new_board, solution = get_game(difficulty)
        request.session['orig_board'] = json.loads(new_board)
        request.session['board'] = json.loads(new_board)
        request.session['solution'] = json.loads(solution)
        request.session['start_time'] = round(time.time())
        if 'end_time' in request.session:
            del request.session['end_time']
        # W = Win, I = In-Progress, L = Lost, S = Surrendered
        request.session['status'] = 'I'
        request.session['hints'] = 0
        return HttpResponseRedirect(reverse('sudoku:play'))


def load_puzzle(request):
    # Written by Ben Brandhorst for Sprint 2, last updated July 3, 2020
    try:
        puzzleid = request.POST['puzzleID']
    except KeyError:
        return render(request, 'sudoku/leaderboard.html', {
            'error_message': 'Please select a puzzle to load.'
        })
    new_board, solution = retrieve_puzzle(puzzleid)
    request.session['player'] = sanitized_player(request.POST['player_name'])
    request.session['orig_board'] = json.loads(new_board)
    request.session['board'] = json.loads(new_board)
    request.session['solution'] = json.loads(solution)
    request.session['start_time'] = round(time.time())
    if 'end_time' in request.session:
        del request.session['end_time']
    # W = Win, I = In-Progress, L = Lost, S = Surrendered
    request.session['status'] = 'I'
    request.session['hints'] = 0
    return HttpResponseRedirect(reverse('sudoku:play'))


def sanitized_diff(diff):
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
    if 0 < int(diff) < 5:  # set upper bound to difficulty level not yet ready
        return str(diff)
    else:
        return False


def sanitized_player(player):
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
    regex = r"^[\w ]{4,20}$"
    match = re.fullmatch(regex, player)
    if match:
        return match[0]
    else:
        return 'Anonymous'

def sanitized_puzzleid(puzzleid):
    # Written by Ben Brandhorst for Sprint 2, last updated July 4, 2020
    regex = r"^[0-9]+$"
    match = re.fullmatch(regex, puzzleid)
    if match:
        return str(puzzleid)
    else:
        return False


def leaderboard(request):
    # Written by Christopher Smith and modified for Sprint 2
    diff1_record1 = calculate_leaders(1)[0]
    diff1_record2 = calculate_leaders(1)[1]
    diff1_record3 = calculate_leaders(1)[2]
    diff1_record4 = calculate_leaders(1)[3]
    diff1_record5 = calculate_leaders(1)[4]
    diff2_record1 = calculate_leaders(2)[0]
    diff2_record2 = calculate_leaders(2)[1]
    diff2_record3 = calculate_leaders(2)[2]
    diff2_record4 = calculate_leaders(2)[3]
    diff2_record5 = calculate_leaders(2)[4]
    diff3_record1 = calculate_leaders(3)[0]
    diff3_record2 = calculate_leaders(3)[1]
    diff3_record3 = calculate_leaders(3)[2]
    diff3_record4 = calculate_leaders(3)[3]
    diff3_record5 = calculate_leaders(3)[4]
    return render(request, 'sudoku/leaderboard.html',
                  {'diff1_record1': diff1_record1,
                   'diff1_record2': diff1_record2,
                   'diff1_record3': diff1_record3,
                   'diff1_record4': diff1_record4,
                   'diff1_record5': diff1_record5,
                   'diff2_record1': diff2_record1,
                   'diff2_record2': diff2_record2,
                   'diff2_record3': diff2_record3,
                   'diff2_record4': diff2_record4,
                   'diff2_record5': diff2_record5,
                   'diff3_record1': diff3_record1,
                   'diff3_record2': diff3_record2,
                   'diff3_record3': diff3_record3,
                   'diff3_record4': diff3_record4,
                   'diff3_record5': diff3_record5})


def play(request):
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
    player = request.session.get('player')
    return render(request, 'sudoku/play.html', {'player': player})


def update_board(request):
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
    end_time = False

    # get JavaScript sessionStorage from POST
    updated_board = json.loads(request.POST.get('board'))
    if corrupted_board(updated_board):
        # user may have tampered with JavaScript Session Data
        return HttpResponse(status=400)

    start_time = json.loads(request.POST.get('start_time'))
    if not isinstance(start_time, int):
        return HttpResponse(status=400)

    status = request.POST.get('status')
    if status not in ['W', 'L', 'I', 'S']:
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

    # uncomment save_game when not using custom board for testing, comment when testing or save will crash
    save_game(data)
    return HttpResponse(status=204)


def corrupted_board(user_board):
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
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
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
    return render(request, 'sudoku/uploadsuccess.html')


class UploadFileForm(forms.Form):
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
    puzzle_file = forms.FileField()


@staff_member_required
def upload(request):
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            read_file(request.FILES['puzzle_file'])
            return HttpResponseRedirect(reverse('sudoku:upload_success'))
    else:
        form = UploadFileForm()
        return render(request, 'sudoku/upload.html', {'form': form})


def get_hint(request):
    # Written by Christopher Breen for Sprint 2, last updated June 29, 2020
    # get JavaScript sessionStorage from POST
    current_board = json.loads(request.POST.get('board'))
    if corrupted_board(current_board):
        # user may have tampered with JavaScript Session Data
        return HttpResponse(status=400)

    # replace length one lists with integers
    current_board = convert_board(current_board, 'Int', False)

    # level 1
    result = naked_single(current_board, hints=True)
    if result:
        return HttpResponse(json.dumps(result))
    result = hidden_single(current_board, hints=True)
    if result:
        return HttpResponse(json.dumps(result))
    # level 2
    result = naked_pair(current_board, hints=True)
    if result:
        return HttpResponse(json.dumps(result))
    result = omission(current_board, hints=True)
    if result:
        return HttpResponse(json.dumps(result))
    result = naked_triplet(current_board, hints=True)
    if result:
        return HttpResponse(json.dumps(result))
    # level 3
    result = hidden_pair(current_board, hints=True)
    if result:
        return HttpResponse(json.dumps(result))
    result = naked_quad(current_board, hints=True)
    if result:
        return HttpResponse(json.dumps(result))
    result = hidden_triplet(current_board, hints=True)
    if result:
        return HttpResponse(json.dumps(result))
    # level 4
    result = hidden_quad(current_board, hints=True)
    if result:
        return HttpResponse(json.dumps(result))
    result = xwing(current_board, hints=True)
    if result:
        return HttpResponse(json.dumps(result))
    result = swordfish(current_board, hints=True)
    if result:
        return HttpResponse(json.dumps(result))


    return HttpResponse(json.dumps(
        'Sorry, your on your own.  You may want to Verify Solutions to see if any mistakes have been made.'))


def convert_board(old_board, direction, orig_board):
    new_board = copy.deepcopy(old_board)
    if direction == 'Int':
        # user solved cells remain as length one lists to differentiate givens from user solved cells
        # This is NOT the case when using techniques to solve puzzles, and will cause issues with hints
        # We must convert single length lists (user solved cells) to integers to find correct hint
        for row in range(9):
            for col in range(9):
                if isinstance(new_board[row][col], list) and len(new_board[row][col]) == 1:
                    new_board[row][col] = new_board[row][col][0]
    elif direction == 'List':
        # convert user solved cells back to length one lists
        for row in range(9):
            for col in range(9):
                if isinstance(new_board[row][col], int) and isinstance(orig_board[row][col], list):
                    new_board[row][col] = [new_board[row][col]]
    return new_board


def erase_obvious(request):
    """Automatically remove all candidates from a cell when that candidate has already been solved in the cell's
    row, column, or block"""
    # It takes 10 minutes of tediously removing numbers from scratchpads before the board is in a state that requires
    # any mental effort.  This function automates the easy stuff so the player can focus on the more challenging
    # techniques.
    orig_board = request.session['orig_board']
    board = convert_board(request.session['board'], 'Int', False)
    progress = True
    while progress:
        progress = naked_single(board)
    board = convert_board(board, 'List', orig_board)
    response = {
        'cleaned_board': board
    }
    return HttpResponse(json.dumps(response))
