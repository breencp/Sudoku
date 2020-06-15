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


def save_game():
    saved_puzzle: Played = Played()
    saved_puzzle.user = Played.user
    saved_puzzle.start_time = Played.start_time
    saved_puzzle.end_time = Played.end_time
    saved_puzzle.saved_board = Played.saved_board
    saved_puzzle.status = Played.status
    saved_puzzle.hints = Played.hints
    try:
        saved_puzzle.save()
    except IntegrityError:
        # user state already exists
        saved_puzzle.save(force_update=True)
