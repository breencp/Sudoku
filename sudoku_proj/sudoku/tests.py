# file: tests.py
# author: Christopher Smith
# date: May 26, 2020

import unittest


class CreateGameTests(unittest.TestCase):

    def accepted_difficulties(self):
        difficulty = ['1', '2', '3', '4', '5', '6']
        board = ""
        solution = ""
        for x in difficulty:
            create_game(x)
            self.assertIs(board, True)
            self.assertIs(solution, True)

    # TODO: execute this when appropriate difficulty constraints are implemented
    def rejected_difficulties(self):
        difficulty = ['0', 'foo', 1]
        board = ""
        solution = ""
        for x in difficulty:
            create_game(x)
            self.assertIs(board, False)
            self.assertIs(solution, False)
