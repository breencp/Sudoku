import copy
import json
import math
import os
import random
import time
from datetime import date

try:
    # this import works when running the django web server
    from .techniques import *
except ImportError:
    try:
        # this import works when running create_game.py in the IDE as main entry point into the program for testing
        from sudoku_proj.sudoku.techniques import *
    except ImportError as err:
        print(err)

# globals (used when making a board solution to reduce random calls and improve efficiency)
avail_row_nums = []
avail_col_nums = []
avail_block_nums = []


def create_game(desired_technique='any', desired_difficulty='1', min_givens=26, max_givens=30):
    """Returns board for user to play, the solution, overall difficulty level, and exact techniques required to win."""
    print('\nCreating solution', end='')
    failed_solves = 0
    while True:
        reset_avail()
        failed_solutions = 0
        while True:
            # make_board returns a complete solution with every cell filled in, or false if it failed
            solution = make_board()
            if solution:
                break
            else:
                # global avail_(row/col_block)_nums get reset to include 1-9 again, then loop
                reset_avail()
                failed_solutions += 1
                if failed_solutions % 200 == 0:
                    print('.', end='')

        print('...done.  Hiding & Solving', end='')
        while True:
            # hide_cells returns the original solution but with a random subset of cell numbers removed
            board = hide_cells(solution, min_givens, max_givens)
            # solvable_puzzle uses techniques in sequentially incremental difficulty attempting to recreate the solution
            solved, actual_difficulty, techniques = solvable_puzzle(copy.deepcopy(board), desired_technique,
                                                                    desired_difficulty)
            if solved:
                # if successful, return the board modified by hide_cells
                print('...done. Iterations to get solution: ' + str(failed_solutions), end='')
                print(', Iterations to solve: ' + str(failed_solves))
                return board, solution, actual_difficulty, techniques
            else:
                failed_solves += 1
                if failed_solves % 10000 == 0:
                    print('\n.', end='')
                elif failed_solves % 100 == 0:
                    print('.', end='')


def hide_cells(solution, min_givens=26, max_givens=30):
    """Returns the complete solution but with a random number (and location) of givens replaced with candidates"""
    # randomly choose number of cells to hide; need minimum 17 visible numbers of 81 total (64 hidden)
    # typical puzzle books indicate 30-33 for easy, 24-31 medium, 17-23 hard
    # puzzles must have at minimum 17 clues to be solvable (64 hidden)
    board = copy.deepcopy(solution)
    givens = random.randint(min_givens, max_givens)
    hide_count = 81 - givens

    counter = 0
    while counter < hide_count:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if not isinstance(board[row][col], list):
            # we grabbed a random row and col, it's not one we have already removed
            counter += 1
            # change the single int to a nested list of pencil marks
            board[row][col] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    return board


def custom_board(human_puzzle):
    """Takes 81 character string of givens and unknowns, returns playable board"""
    # convert human readable board sequence into multidimensional list used in code.  e.g. follows:
    # 9?67853???????65???8?3216??43??5?9786?????25?????6???5??85???2??4?1?8???
    # The sequence above represents the known numbers and unknown numbers in the puzzle.  It can be read from
    # a text file used for testing techniques, or could be input by the user to play a custom board.
    # it starts in upper left most cell and reads left to right, top to bottom.

    # makes a 9x9 multi-dimensional list of zeros
    board = [[0 for x in range(9)] for x in range(9)]
    for i in range(len(human_puzzle)):
        row = math.floor(i / 9)
        col = i % 9
        if human_puzzle[i] == '?' or human_puzzle[i] == ' ':
            board[row][col] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        else:
            board[row][col] = int(human_puzzle[i])
    return board


def reset_avail():
    """Resets avail row/col/block nums to [1, 2, 3, 4, 5, 7, 8, 9]"""
    global avail_block_nums
    global avail_col_nums
    global avail_row_nums
    avail_row_nums = [[x for x in range(1, 10)] for y in range(1, 10)]
    avail_col_nums = [[x for x in range(1, 10)] for y in range(1, 10)]
    avail_block_nums = [[x for x in range(1, 10)] for y in range(1, 10)]


def make_board():
    """Returns a valid sudoku solution, i.e. 9x9 of [1-9] with no dup nums in row, col, or block"""
    # Makes a 9x9 multi-dimensional list of zeros
    board = [[0 for x in range(9)] for x in range(9)]

    for row in range(9):
        for col in range(9):
            # figure out what block we are in
            block = get_block(row, col)
            # start with 1-9, and remove any number that already exists in current row, col, and block
            avail_nums = get_avail_nums(row, col, block)
            if not avail_nums:
                # There are no numbers left to choose from, so the puzzle is invalid, need to start over
                return False
            # select a random int from the list of remaining avail nums
            i = avail_nums[random.randint(0, len(avail_nums) - 1)]
            # set this cell of the board to that random int and remove availability for this row, col, and block
            board[row][col] = i
            avail_row_nums[row].remove(i)
            avail_col_nums[col].remove(i)
            avail_block_nums[block].remove(i)

    return board


def get_block(row, col):
    """Determine what block provided row and col are in"""
    if row <= 2:
        if col <= 2:
            return 0
        elif col <= 5:
            return 1
        elif col <= 8:
            return 2
    elif row <= 5:
        if col <= 2:
            return 3
        elif col <= 5:
            return 4
        elif col <= 8:
            return 5
    elif row <= 8:
        if col <= 2:
            return 6
        elif col <= 5:
            return 7
        elif col <= 8:
            return 8


def get_avail_nums(row, col, block):
    """Returns list of numbers not already used in the row, col, or block"""
    avail = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for x in range(1, 10):
        if x not in avail_row_nums[row] and x in avail:
            avail.remove(x)
        if x not in avail_col_nums[col] and x in avail:
            avail.remove(x)
        if x not in avail_block_nums[block] and x in avail:
            avail.remove(x)
    return avail


def board_to_string(board):
    """Converts the board from multidimensional list to a string for seeding into sudoku-solutions.com to verify/test.
    Also returns number of givens in the puzzle."""
    board_string = ''
    givens = 0
    for row in range(9):
        for col in range(9):
            if isinstance(board[row][col], list):
                board_string += ' '
            else:
                board_string += str(board[row][col])
                givens += 1
    return board_string, givens


if __name__ == "__main__":
    """create_game.py is designed to be run in the local IDE.  It creates puzzles and stores them in a JSON file for
    later import into the database using 0.0.0.0/sudoku/upload by a Django Admin"""

    custom = False
    # used to test techniques with custom boards, comment out below to get random boards instead
    # custom = custom_board('?5736?2846?4825???28?7?465??924?6???3619?7?42?45132?964?62???75?2?57?46?57864?32?')

    # set desired_technique (or desired difficulty) to:
    # Level 1: naked_single, hidden_single
    # Level 2: naked_pair, omission, naked_triplet
    # Level 3: hidden_pair, hidden_triplet, naked_quad
    # Level 4: hidden_quad, x_wing, swordfish
    # Any Level: 'any'
    desired_technique = 'any'
    desired_difficulty = '3'

    # how many puzzles to find before breaking loop
    puzzles_to_create = 10

    # choose the bounds for number of givens in the puzzle.  Generally, fewer givens are considered more challenging
    # puzzles, but really it's about the techniques.  Puzzles are easier to generate with 28-30 givens.  Expanding
    # the lower bound will take significantly longer to discover a valid puzzle, but may yield a great one every now
    # and then.
    min_givens = 28
    max_givens = 30

    if custom:
        print(custom)
        # solvable_puzzle uses techniques in sequentially incremented difficulty levels in an attempt to solve
        print(solvable_puzzle(copy.deepcopy(custom)))
    else:
        start = time.time()
        for i in range(puzzles_to_create):
            # create_game will loop until it creates a puzzle we want to break on for testing
            board, solution, actual_difficulty, techniques = create_game(desired_technique, desired_difficulty,
                                                                         min_givens, max_givens)
            board_string, givens = board_to_string(board)
            data = {'board': board,
                    'solution': solution,
                    'difficulty': actual_difficulty,
                    'techniques': techniques,
                    'givens': givens,
                    'board_string': board_string
                    }

            # save puzzles in JSON format to a filename of today's date to keep them organized
            dev_name = os.environ.get('LOGNAME')
            if not dev_name:
                dev_name = 'anon'
            filename = 'puzzles/' + date.today().strftime('%Y%m%d_') + dev_name + '.json'
            with open(filename, 'a+') as f:
                json.dump(data, f)
                f.write('\n')
            f.close()

            end = time.time()
            output = '#', i, '- Difficulty:', data['difficulty'], data['techniques'], '- Givens:', givens, \
                     '- Total hours elapsed:', round((end - start) / 3600, 2)
            print(*output)
            print(board_string)
