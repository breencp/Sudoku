# file: gamerecords.py
# author: Christopher Smith
# date: 12 June 2020
from django.db import IntegrityError

from .models import Puzzles, Played


def read_file(f):
    for row in f:
        data = eval(row)
        new_puzzle = Puzzles()
        new_puzzle.board = data['board']
        new_puzzle.solution = data['solution']
        new_puzzle.difficulty = data['difficulty']
        for technique, value in data['techniques'].items():
            setattr(new_puzzle, technique, value)
        try:
            new_puzzle.save()
        except IntegrityError:
            # unique constraint failed, puzzle already exists
            pass


def get_game(difficulty):
    puzzles = Puzzles.objects.filter(difficulty=difficulty).order_by('?')[0]
    return puzzles.board, puzzles.solution


def save_game(data):
    saved_puzzle: Played = Played()
    saved_puzzle.user = data['user']
    saved_puzzle.start_time = round(data['start_time'])
    if 'end_time' in data:
        saved_puzzle.end_time = round(data['end_time'])
    saved_puzzle.status = data['status']
    saved_puzzle.hints = data['hints']
    saved_puzzle.saved_board = data['current_board']
    orig_board = data['orig_board']
    saved_puzzle.puzzle_id = Puzzles.objects.filter(board=orig_board).order_by('puzzle_id')[0]
    query = Played.objects.filter(puzzle_id=saved_puzzle.puzzle_id,
                                  user=saved_puzzle.user, start_time=saved_puzzle.start_time)
    # update an existing entry
    if query:
        query.update(saved_board=saved_puzzle.saved_board)
    # create a new entry
    else:
        saved_puzzle.save()
