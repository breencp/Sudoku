# file: tests.py
# author: Christopher Smith
# date: May 26, 2020

# TODO: allow executability without commenting out the following line
# from django.test import TestCase
import random
from sudoku_proj.sudoku.create_game import make_board
from sudoku_proj.sudoku.create_game import create_game
from sudoku_proj.sudoku.create_game import hide_cells
from sudoku_proj.sudoku.create_game import get_block
from sudoku_proj.sudoku.create_game import get_avail_nums

# globals for create_game.py unit tests
avail_row_nums = []
avail_col_nums = []
avail_block_nums = []

# TODO: delete this once get_available_nums test is fixed?
# inclusion of reset_avail as it is untestable
def reset_avail():
    # resets avail row/col/block nums to [1, 2, 3, 4, 5, 7, 8, 9]
    global avail_block_nums
    global avail_col_nums
    global avail_row_nums
    avail_row_nums = [[x for x in range(1, 10)] for y in range(1, 10)]
    avail_col_nums = [[x for x in range(1, 10)] for y in range(1, 10)]
    avail_block_nums = [[x for x in range(1, 10)] for y in range(1, 10)]

# create_game.py unit test: get_block
row = [0, 1, 2, 3, 4, 5, 6, 7, 8]
col = [0, 1, 2, 3, 4, 5, 6, 7, 8]
for row in range(9):
    for col in range(9):
        block = get_block(row, col)
        if 0 or 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8:
            print("Block retrieval succeeded.")
        else:
            print("Block retrieval failed.")

# create_game.py unit test: get_available_nums
avail = [1, 2, 3, 4, 5, 6, 7, 8, 9]
get_avail_nums(row, col, block)
if avail:
    print("Available number retrieval succeeded.")
else:
    print("Available number retrieval failed.")

# create_game.py unit test: make_board
board = ""
row = random.randint(0, 8)
col = random.randint(0, 8)
make_board()
if board:
    print("Board creation succeeded.")
else:
    print("Board creation failed.")

# create_game.py unit test: hide_cells
solution = make_board()
hide_cells(solution, '1')
if board:
    print("Cell hiding succeeded.")
else:
    print("Cell hiding failed.")

# create_game.py unit test: create_game--Difficulty 1
avail_row_nums = [[x for x in range(1, 10)] for y in range(1, 10)]
avail_col_nums = [[x for x in range(1, 10)] for y in range(1, 10)]
avail_block_nums = [[x for x in range(1, 10)] for y in range(1, 10)]
create_game('1')
if board:
    print("Game creation succeeded.")
else:
    print("Game creation failed.")