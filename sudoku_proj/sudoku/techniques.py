# file: techniques.py
# author: Christopher Breen
# date:
import copy
import math


def solvable_puzzle(puzzle_to_solve):
    """Returns true if able to solve provided puzzle with provided difficulty level"""
    progress = True
    techniques_utilized = dict()
    actual_difficulty = '1'
    while progress:
        progress = False

        # Difficulty Level 1
        # Naked Single: only technique that solves more than one within function
        if naked_single(puzzle_to_solve):
            techniques_utilized.update({'naked_single': 'True'})
            progress = True
        # Hidden Single
        if hidden_single(puzzle_to_solve):
            techniques_utilized.update({'hidden_single': 'True'})
            progress = True

        # Difficulty Level 2
        # Naked Pair: repeatedly try easier techniques until no longer making progress without advanced techniques
        if not progress:
            if naked_pair(puzzle_to_solve):
                techniques_utilized.update({'naked_pair': 'True'})
                if actual_difficulty < '2':
                    actual_difficulty = '2'
                progress = True
        # Omission (a.k.a. Intersection, Pointing)
        if not progress:
            if omission(puzzle_to_solve):
                techniques_utilized.update({'omission': 'True'})
                if actual_difficulty < '2':
                    actual_difficulty = '2'
                progress = True
        # Naked Triplet

        # Level 3 Difficulty
        # Hidden Pair
        # Naked Quad
        # Hidden Triplet

        # Level 4 Difficulty
        # Hidden Quad
        # X-Wing
        # Swordfish
        # XY-Wing
        # Unique Rectangle

    # we have continually looped through all techniques in the given difficulty level
    # we may or may not have removed all available numbers down to a single int.  Let's check.
    # if is_solved(puzzle_to_solve):  # test code, replace with line below
    if is_solved(puzzle_to_solve):
        return True, actual_difficulty, techniques_utilized
    else:
        return False, False, False


def naked_single(solving_puzzle):
    """Naked Single removes any number found in the current row, col, and block.  If only one single number remains,
    it is the solution to that cell"""
    progress = True
    overall_progress = False
    while progress:
        progress = False
        for row in range(9):
            for col in range(9):
                if isinstance(solving_puzzle[row][col], list):
                    # this is an unsolved cell
                    nums_used = set()
                    for i in range(9):
                        if i is not col and not isinstance(solving_puzzle[row][i], list):
                            nums_used.add(solving_puzzle[row][i])
                        if i is not row and not isinstance(solving_puzzle[i][col], list):
                            nums_used.add(solving_puzzle[i][col])
                    yi, xi = get_upper_left(row, col)
                    for y in range(yi, yi + 3):
                        for x in range(xi, xi + 3):
                            if not (x is col and y is row) and not isinstance(solving_puzzle[y][x], list):
                                nums_used.add(solving_puzzle[y][x])
                    for digit in nums_used:
                        if digit in solving_puzzle[row][col]:
                            solving_puzzle[row][col].remove(digit)
                            progress = True
                            overall_progress = True
                            # print([row][0]), [col][0], solving_puzzle[row][col]
                    if solved_cell(solving_puzzle, row, col):
                        # other techniques need to be exited to allow cleanup by naked_single
                        pass
    return overall_progress


def hidden_single(solving_puzzle):
    """Hidden single looks at the pencil marks in each cell and then each cell within the row/col/block to
    see if it contains a number that is not contained in pencil marks of any other cell in the row/col/block"""
    for row in range(9):
        for col in range(9):
            if isinstance(solving_puzzle[row][col], list):
                # this is an unsolved cell, get avail nums remaining
                cell_possibles = solving_puzzle[row][col][:]
                for i in range(len(cell_possibles)):
                    single = True
                    for x in range(9):
                        if x is not col and isinstance(solving_puzzle[row][x], list):
                            if cell_possibles[i] in solving_puzzle[row][x]:
                                single = False
                    if single:
                        # print([row], [col], 'Hidden Single: ', cell_possibles[i])
                        solving_puzzle[row][col] = cell_possibles[i]
                        return True

                    single = True
                    for y in range(9):
                        if y is not row and isinstance(solving_puzzle[y][col], list):
                            if cell_possibles[i] in solving_puzzle[y][col]:
                                single = False
                    if single:
                        # print([row], [col], 'Hidden Single: ', cell_possibles[i])
                        solving_puzzle[row][col] = cell_possibles[i]
                        return True

                    single = True
                    yi, xi = get_upper_left(row, col)
                    for y in range(yi, yi + 3):
                        for x in range(xi, xi + 3):
                            if not (x is col and y is row) and isinstance(solving_puzzle[y][x], list):
                                if cell_possibles[i] in solving_puzzle[y][x]:
                                    single = False
                    if single:
                        # print([row], [col], 'Hidden Single: ', cell_possibles[i])
                        solving_puzzle[row][col] = cell_possibles[i]
                        return True

    return False


def naked_pair(solving_puzzle):
    """Naked Pair looks for two cells with an identical pair of remaining numbers.
    These numbers can be removed from any other cell in the col, row, or block."""
    progress = False
    for row in range(9):
        for col in range(9):
            if isinstance(solving_puzzle[row][col], list):
                if len(solving_puzzle[row][col]) == 2:
                    pairs = 1
                    for x in range(9):
                        if x is not col and solving_puzzle[row][col] == solving_puzzle[row][x]:
                            pairs += 1
                            col2 = copy.copy(x)
                    if pairs == 2:
                        # found naked pair in row, remove numbers from rest of row
                        for x in range(9):
                            if x is not col and x is not col2 and isinstance(solving_puzzle[row][x], list):
                                if solving_puzzle[row][col][0] in solving_puzzle[row][x]:
                                    solving_puzzle[row][x].remove(solving_puzzle[row][col][0])
                                    progress = True
                                    if not solved_cell(solving_puzzle, row, x):
                                        if solving_puzzle[row][col][1] in solving_puzzle[row][x]:
                                            solving_puzzle[row][x].remove(solving_puzzle[row][col][1])
                                            solved_cell(solving_puzzle, row, x)
                        # if both pairs are in same block we can remove from the rest of the block too
                        if get_upper_left(row, col) == get_upper_left(row, col2):
                            yi, xi = get_upper_left(row, col)
                            for y in range(yi, yi + 3):
                                for x in range(xi, xi + 3):
                                    if not (x is col and y is row) and not (x is col2 and y is row) and isinstance(
                                            solving_puzzle[y][x], list):
                                        if solving_puzzle[row][col][0] in solving_puzzle[y][x]:
                                            solving_puzzle[y][x].remove(solving_puzzle[row][col][0])
                                            progress = True
                                            if not solved_cell(solving_puzzle, y, x):
                                                if solving_puzzle[row][col][1] in solving_puzzle[y][x]:
                                                    solving_puzzle[y][x].remove(solving_puzzle[row][col][1])
                                                    solved_cell(solving_puzzle, y, x)
                        if progress:
                            return True

                    pairs = 1
                    for y in range(9):
                        if y is not row and solving_puzzle[row][col] == solving_puzzle[y][col]:
                            pairs += 1
                            row2 = copy.copy(y)
                    if pairs == 2:
                        # found naked pair in col, remove numbers from rest of col
                        for y in range(9):
                            if y is not row and y is not row2 and isinstance(solving_puzzle[y][col], list):
                                if solving_puzzle[row][col][0] in solving_puzzle[y][col]:
                                    solving_puzzle[y][col].remove(solving_puzzle[row][col][0])
                                    progress = True
                                    if not solved_cell(solving_puzzle, y, col):
                                        if solving_puzzle[row][col][1] in solving_puzzle[y][col]:
                                            solving_puzzle[y][col].remove(solving_puzzle[row][col][1])
                                            solved_cell(solving_puzzle, y, col)
                        # if both pairs are in same block we can remove from the rest of the block too
                        if get_upper_left(row, col) == get_upper_left(row2, col):
                            yi, xi = get_upper_left(row, col)
                            for y in range(yi, yi + 3):
                                for x in range(xi, xi + 3):
                                    if not (x is col and y is row) and not (x is col and y is row2) and isinstance(
                                            solving_puzzle[y][x], list):
                                        if solving_puzzle[row][col][0] in solving_puzzle[y][x]:
                                            solving_puzzle[y][x].remove(solving_puzzle[row][col][0])
                                            progress = True
                                            if not solved_cell(solving_puzzle, y, x):
                                                if solving_puzzle[row][col][1] in solving_puzzle[y][x]:
                                                    solving_puzzle[y][x].remove(solving_puzzle[row][col][1])
                                                    solved_cell(solving_puzzle, y, x)
    return progress


def omission(solving_puzzle):
    # if the only cells in a row for a given number lie in the same block,
    # all other cells in the block must not contain that number
    progress = False
    for num in range(1, 9):
        for row in range(9):
            # scanning new row, reset block details
            constrained_to_block = True
            by = -1
            bx = -1
            for col in range(9):
                if isinstance(solving_puzzle[row][col], list):
                    if num in solving_puzzle[row][col]:
                        this_by, this_bx = get_upper_left(row, col)
                        if by == -1 and bx == -1:
                            by = this_by
                            bx = this_bx
                        else:
                            if bx is not this_bx or by is not this_by:
                                # number spans multiple blocks within row
                                constrained_to_block = False
                                break  # can stop looking at row
                else:
                    if solving_puzzle[row][col] == num:
                        # num already solved
                        constrained_to_block = False  # technically not true but we can ignore this num
                        break  # this number is solved
            if constrained_to_block:
                for y in range(by, by + 3):
                    if y is not row:  # skip over row we found the number in
                        for x in range(bx, bx + 3):
                            if isinstance(solving_puzzle[y][x], list):
                                if num in solving_puzzle[y][x]:
                                    solving_puzzle[y][x].remove(num)
                                    # print(*'#', num, 'f', y, x, end='')
                                    progress = True
                                    if solved_cell(solving_puzzle, y, x):
                                        # naked_single must cleanup puzzle
                                        return progress

    # if the only cells in a column for a given number lie in the same block,
    # all other cells in the block must not contain that number
    for num in range(1, 9):
        for col in range(9):
            # scanning new col, reset block details
            constrained_to_block = True
            by = -1
            bx = -1
            for row in range(9):
                if isinstance(solving_puzzle[row][col], list):
                    if num in solving_puzzle[row][col]:
                        this_by, this_bx = get_upper_left(row, col)
                        if by == -1 and bx == -1:
                            by = this_by
                            bx = this_bx
                        else:
                            if bx is not this_bx or by is not this_by:
                                # number spans multiple blocks within row
                                constrained_to_block = False
                                break  # can stop looking at row
                else:
                    if solving_puzzle[row][col] == num:
                        # num already solved
                        constrained_to_block = False  # technically not true but we can ignore this num
                        break  # this number is solved
            if constrained_to_block:
                for x in range(bx, bx + 3):
                    if x is not col:  # skip over row we found the number in
                        for y in range(by, by + 3):
                            if isinstance(solving_puzzle[y][x], list):
                                if num in solving_puzzle[y][x]:
                                    solving_puzzle[y][x].remove(num)
                                    # print(*'#', num, 'f', y, x, end='')
                                    progress = True
                                    if solved_cell(solving_puzzle, y, x):
                                        return progress

    # if the only cells in a block for a given number lie in the same row,
    # all other cells in the row must not contain that number
    for num in range(1, 9):
        for block in range(9):
            # block 0, 1, 2: y = 0, x = 0, 3, 6
            # block 3, 4, 5: y = 3, x = 0, 3, 6
            # block 6, 7, 8: y = 6, x = 0, 3, 6
            by = math.floor(block / 3) * 3
            bx = (block % 3) * 3
            row = -1
            constrained_to_row = True
            for y in range(by, by + 3):
                if not constrained_to_row:
                    # already spans 2 rows, no need to check the third row
                    break
                for x in range(bx, bx + 3):
                    if isinstance(solving_puzzle[y][x], list):
                        if num in solving_puzzle[y][x]:
                            if row == -1:
                                row = y
                            else:
                                if row is not y:
                                    # number spans multiple rows within block
                                    constrained_to_row = False
                                    break  # can stop looking for num; breaking from remainder of row
                    else:
                        # check to see if our num is already solved
                        if solving_puzzle[y][x] is num:
                            break
            if constrained_to_row and row != -1:
                for x in range(9):
                    if isinstance(solving_puzzle[row][x], list):
                        if x not in [bx, bx + 1, bx + 2]:
                            # we are not in the block of constrained number
                            if num in solving_puzzle[row][x]:
                                solving_puzzle[row][x].remove(num)
                                # print(*'#', num, 'f', row, x, end='')
                                progress = True
                                if solved_cell(solving_puzzle, row, x):
                                    return progress

# if the only cells in a block for a given number lie in the same column,
# all other cells in the column must not contain that number
    for num in range(1, 9):
        for block in range(9):
            # block 0, 1, 2: y = 0, x = 0, 3, 6
            # block 3, 4, 5: y = 3, x = 0, 3, 6
            # block 6, 7, 8: y = 6, x = 0, 3, 6
            by = math.floor(block / 3) * 3
            bx = (block % 3) * 3
            col = -1
            constrained_to_col = True
            for x in range(bx, bx + 3):
                if not constrained_to_col:
                    # already spans 2 rows, no need to check the third row
                    break
                for y in range(by, by + 3):
                    if isinstance(solving_puzzle[y][x], list):
                        if num in solving_puzzle[y][x]:
                            if col == -1:
                                col = x
                            else:
                                if col is not x:
                                    # number spans multiple rows within block
                                    constrained_to_col = False
                                    break  # can stop looking for num; breaking from remainder of row
                    else:
                        # check to see if our num is already solved
                        if solving_puzzle[y][x] is num:
                            break
            if constrained_to_col and col != -1:
                for y in range(9):
                    if isinstance(solving_puzzle[y][col], list):
                        if y not in [by, by + 1, by + 2]:
                            # we are not in the block of constrained number
                            if num in solving_puzzle[y][col]:
                                solving_puzzle[y][col].remove(num)
                                # print(*'#', num, 'f', y, col, end='')
                                progress = True
                                if solved_cell(solving_puzzle, y, col):
                                    return progress

    return progress


def get_upper_left(row, col):
    """Returns row and col of upper left cell in block"""
    if row < 3:
        yi = 0
    elif row < 6:
        yi = 3
    else:
        yi = 6
    if col < 3:
        xi = 0
    elif col < 6:
        xi = 3
    else:
        xi = 6
    return yi, xi


def is_solved(puzzle):
    for row in range(9):
        for col in range(9):
            if isinstance(puzzle[row][col], list):
                return False
    return True


def solved_cell(solving_puzzle, y, x):
    # we removed a number from the scratchpad.
    # if there is only one number remaining we must convert type of cell from list of length one into an integer
    # otherwise we run into problems in various techniques looking for cells with multiple options remaining
    if len(solving_puzzle[y][x]) == 1:
        solving_puzzle[y][x] = solving_puzzle[y][x][0]
        return True
    return False
