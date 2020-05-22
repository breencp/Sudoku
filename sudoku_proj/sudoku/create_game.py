# file: create_game.py
# author: Christopher Breen
# date: May 21, 2020

import random
import time

# globals
avail_row_nums = []
avail_col_nums = []
avail_block_nums = []


def hide_cells(solution, difficulty):
    # randomly choose number of cells to hide; need minimum 17 visible numbers of 81 total (64 hidden)
    # typical puzzle books indicate 30-33 for easy, 24-31 medium
    board = solution

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
        if board[row][col] > 0:
            counter += 1
            board[row][col] = 0

    return board


def create_game(difficulty):
    counter = 0  # debug purposes to determine how many iterations it takes to get a valid board
    reset_avail()
    while True:
        solution = make_board()
        if solution:
            print("Iterations Required: ", counter)  # TODO: remove debug code
            # we now have a complete board solution
            # let's hide some cells and attempt to solve to determine difficulty level

            break
        else:
            reset_avail()
            counter += 1

    board = hide_cells(solution, difficulty)
    return board


def reset_avail():
    global avail_block_nums
    global avail_col_nums
    global avail_row_nums
    avail_row_nums = [[x for x in range(1, 10)] for y in range(1, 10)]
    avail_col_nums = [[x for x in range(1, 10)] for y in range(1, 10)]
    avail_block_nums = [[x for x in range(1, 10)] for y in range(1, 10)]


def make_board():
    board = [[0 for x in range(9)] for x in range(9)]

    for row in range(9):
        for col in range(9):
            block = get_block(row, col)
            avail_nums = get_avail_nums(row, col, block)
            if not avail_nums:
                return False
            i = avail_nums[random.randint(0, len(avail_nums) - 1)]
            board[row][col] = i
            avail_row_nums[row].remove(i)
            avail_col_nums[col].remove(i)
            avail_block_nums[block].remove(i)

    return board


def get_block(row, col):
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
    # benchmark compute times to create boards, ensure within acceptable parameters
    start = time.time()
    print(*create_game('1'), sep="\n")
    end = time.time()
    print("Elapsed: ", (end - start))


if __name__ == "__main__":
    create_game_debug()
