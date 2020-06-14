# file: gamerecords.py
# author: Christopher Smith
# date: 12 June 2020

from sudoku_proj.sudoku.models import Puzzles


def read_file():
    lines = open("puzzles/20200611.txt", "r")
    for x in lines:
        Puzzles(x)


if __name__ == '__main__':
    read_file()
