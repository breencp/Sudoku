# file: create_game.py
# author: Christopher Breen
# date: May 21, 2020
import copy
import random
import time
from .techniques import solvable_puzzle


# globals
avail_row_nums = []
avail_col_nums = []
avail_block_nums = []


def create_game(difficulty):
    print('Creating game...', end='')
    while True:
        print('.', end='')
        reset_avail()
        while True:
            # make_board returns a complete solution will every cell filled in
            solution = make_board()
            if solution:
                break
            else:
                # global avail_(row/col_block)_nums get reset to include 1-9 again
                reset_avail()

        # hide_cells returns the original solution but with a random subset of cell numbers removed
        board = hide_cells(solution, difficulty)
        # solvable_puzzle uses techniques in requested difficulty to level in an attempt to recreate the solution
        if solvable_puzzle(copy.deepcopy(board), difficulty):
            # if successful, return the board modified by hide_cells
            return board


def hide_cells(solution, difficulty):
    # randomly choose number of cells to hide; need minimum 17 visible numbers of 81 total (64 hidden)
    # typical puzzle books indicate 30-33 for easy, 24-31 medium
    board = copy.deepcopy(solution)

    # front-end passes string number values for difficulty to allow easy changing of level names
    if difficulty == '1':
        hide_count = random.randint(48, 53)
    elif difficulty == '2':
        hide_count = random.randint(53, 58)
    elif difficulty == '3':
        hide_count = random.randint(58, 63)
    elif difficulty == '4':
        hide_count = 64
    elif difficulty == '5':
        hide_count = 64
    else:
        hide_count = 50

    counter = 0
    while counter < hide_count:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if not isinstance(board[row][col], list):
            # we grabbed a random row and col, and it's not once we have already removed
            counter += 1
            # change the single int to a nested list of pencil marks
            board[row][col] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    return board


def reset_avail():
    # resets avail row/col/block nums to [1, 2, 3, 4, 5, 7, 8, 9]
    global avail_block_nums
    global avail_col_nums
    global avail_row_nums
    avail_row_nums = [[x for x in range(1, 10)] for y in range(1, 10)]
    avail_col_nums = [[x for x in range(1, 10)] for y in range(1, 10)]
    avail_block_nums = [[x for x in range(1, 10)] for y in range(1, 10)]


def make_board():
    # makes a 9x9 multi-dimensional list of zeros
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
    """determine what block provided row and col are in"""
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
    avail = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for x in range(1, 10):
        if x not in avail_row_nums[row] and x in avail:
            avail.remove(x)
        if x not in avail_col_nums[col] and x in avail:
            avail.remove(x)
        if x not in avail_block_nums[block] and x in avail:
            avail.remove(x)
    return avail


def create_game_debug():
    """benchmark compute times to create boards, ensure within acceptable parameters"""
    # TODO: remove from production code
    start = time.time()
    print(*create_game('1'), sep="\n")
    end = time.time()
    print("Seconds to generate: ", (end - start))


if __name__ == "__main__":
    create_game_debug()
