# file: tests.py
# author: Christopher Smith
# date: May 26, 2020

# TODO: allow executability without commenting out the following line
# from django.test import TestCase

from sudoku_proj.sudoku.create_game import create_game


def accepted_difficulties():
    difficulty = ['1', '2', '3', '4', '5', '6']
    for x in difficulty:
        result = create_game(x)
        if result:
            print('Successfully created game with difficulty ' + x + '\n')
        else:
            print('Failed to create game with difficulty ' + x + '\n')


# TODO: execute this when appropriate difficulty constraints are implemented
def rejected_difficulties():
    difficulty = ['0', 'foo', 1]
    for x in difficulty:
        result = create_game(x)
        if result:
            print('Successfully create game with difficulty ' + x + '\n')
        else:
            print('Failed to create game with difficulty ' + x + '\n')
