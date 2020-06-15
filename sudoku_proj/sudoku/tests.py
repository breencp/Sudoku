# file: tests.py
# author: Christopher Smith
# date: May 26, 2020

import unittest

from sudoku_proj.sudoku import create_game as cg


class CreateGameTests(unittest.TestCase):

    def accepted_difficulties(self):
        difficulty = ['1', '2', '3', '4', '5', '6']
        board = ""
        solution = ""
        for x in difficulty:
            cg.create_game()
            self.assertIs(board, True)
            self.assertIs(solution, True)

    # TODO: execute this when appropriate difficulty constraints are implemented
    def rejected_difficulties(self):
        difficulty = ['0', 'foo', 1]
        board = ""
        solution = ""
        for x in difficulty:
            cg.create_game()
            self.assertIs(board, False)
            self.assertIs(solution, False)
