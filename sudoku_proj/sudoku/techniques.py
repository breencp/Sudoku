# file: techniques.py
# author: Christopher Breen
# last updated: July 3, 2020
import copy
import math

from .create_game import get_block


def solvable_puzzle(puzzle_to_solve):
    """Returns true if able to solve provided puzzle with provided difficulty level"""
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
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
        # Naked Pair
        if not progress:  # repeatedly try easier techniques until no longer making progress without advanced techniques
            if naked_pair(puzzle_to_solve):
                techniques_utilized.update({'naked_pair': 'True'})
                progress = True
                if actual_difficulty < '2':
                    actual_difficulty = '2'
        # Omission (a.k.a. Intersection, Pointing)
        if not progress:
            if omission(puzzle_to_solve):
                techniques_utilized.update({'omission': 'True'})
                progress = True
                if actual_difficulty < '2':
                    actual_difficulty = '2'
        # Naked Triplet
        if not progress:
            if naked_triplet(puzzle_to_solve):
                techniques_utilized.update({'naked_triplet': 'True'})
                progress = True
                if actual_difficulty < '2':
                    actual_difficulty = '2'

        # Level 3 Difficulty
        # Hidden Pair
        if not progress:
            if hidden_pair(puzzle_to_solve):
                techniques_utilized.update({'hidden_pair': 'True'})
                progress = True
                if actual_difficulty < '3':
                    actual_difficulty = '3'
        # Naked Quad
        if not progress:
            if naked_quad(puzzle_to_solve):
                techniques_utilized.update({'naked_quad': 'True'})
                progress = True
                if actual_difficulty < '3':
                    actual_difficulty = '3'
        # Hidden Triplet
        if not progress:
            if hidden_triplet(puzzle_to_solve):
                techniques_utilized.update({'hidden_triplet': 'True'})
                progress = True
                if actual_difficulty < '3':
                    actual_difficulty = '3'

        # Level 4 Difficulty
        # Hidden Quad
        if not progress:
            if hidden_quad(puzzle_to_solve):
                techniques_utilized.update({'hidden_quad': 'True'})
                progress = True
                if actual_difficulty < '4':
                    actual_difficulty = '4'

        # X-Wing
        # Swordfish
        # XY-Wing
        # Unique Rectangle

    # we have continually looped through all techniques in the given difficulty level
    # we may or may not have removed all available numbers down to a single int.  Let's check.
    if is_solved(puzzle_to_solve):
        return True, actual_difficulty, techniques_utilized
    else:
        return False, False, False


def naked_single(solving_puzzle, hints=False):
    """Naked Single removes any number found in the current row, col, and block.  If only one single number remains,
    it is the solution to that cell"""
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
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
                            if hints:
                                return 'Row ' + str(row + 1) + ', Col ' + str(col + 1) + \
                                       ' contains a candidate that has already been solved in the same ' \
                                       'row, column, or block.'
                            else:
                                solving_puzzle[row][col].remove(digit)
                                progress = True
                                overall_progress = True
                    if not hints:
                        solved_cell(solving_puzzle, row, col)

    return overall_progress


def hidden_single(solving_puzzle, hints=False):
    """Hidden single looks at the pencil marks in each cell and then each cell within the row/col/block to
    see if it contains a number that is not contained in pencil marks of any other cell in the row/col/block"""
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
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
                        if hints:
                            return 'There is a Hidden Single in Row ' + str(row + 1)
                        else:
                            solving_puzzle[row][col] = cell_possibles[i]
                            return True

                    single = True
                    for y in range(9):
                        if y is not row and isinstance(solving_puzzle[y][col], list):
                            if cell_possibles[i] in solving_puzzle[y][col]:
                                single = False
                    if single:
                        if hints:
                            return 'There is a Hidden Single in Column ' + str(col + 1)
                        else:
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
                        if hints:
                            return 'There is a Hidden Single in Block ' + str(get_block(row, col) + 1)
                        else:
                            solving_puzzle[row][col] = cell_possibles[i]
                            return True

    return False


def naked_pair(solving_puzzle, hints=False):
    """Naked Pair looks for two cells with an identical pair of remaining numbers.
    These numbers can be removed from any other cell in the col, row, or block."""
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
    progress = False
    for row in range(9):
        for col in range(9):
            if isinstance(solving_puzzle[row][col], list):
                if len(solving_puzzle[row][col]) == 2:
                    # found a pair, look in row for another identical pair
                    pairs = 1
                    for x in range(9):
                        if x != col and solving_puzzle[row][col] == solving_puzzle[row][x]:
                            pairs += 1
                            col2 = copy.copy(x)
                    if pairs == 2:
                        # found naked pair in row, remove numbers from rest of row
                        for x in range(9):
                            if x != col and x != col2 and isinstance(solving_puzzle[row][x], list):
                                if solving_puzzle[row][col][0] in solving_puzzle[row][x]:
                                    if hints:
                                        return 'There is a Naked Pair in Row ' + str(row + 1)
                                    else:
                                        solving_puzzle[row][x].remove(solving_puzzle[row][col][0])
                                        progress = True
                                if not solved_cell(solving_puzzle, row, x):
                                    if solving_puzzle[row][col][1] in solving_puzzle[row][x]:
                                        if hints:
                                            return 'There is a Naked Pair in Row ' + str(row + 1)
                                        else:
                                            solving_puzzle[row][x].remove(solving_puzzle[row][col][1])
                                            progress = True
                                            solved_cell(solving_puzzle, row, x)
                        if progress:
                            # clean up with easier techniques before continuing
                            return True

                    # look in column for another identical pair
                    pairs = 1
                    for y in range(9):
                        if y != row and solving_puzzle[row][col] == solving_puzzle[y][col]:
                            pairs += 1
                            row2 = copy.copy(y)
                    if pairs == 2:
                        # found naked pair in col, remove numbers from rest of col
                        for y in range(9):
                            if y != row and y != row2 and isinstance(solving_puzzle[y][col], list):
                                if solving_puzzle[row][col][0] in solving_puzzle[y][col]:
                                    if hints:
                                        return 'There is a Naked Pair in Column ' + str(col + 1)
                                    else:
                                        solving_puzzle[y][col].remove(solving_puzzle[row][col][0])
                                        progress = True
                                if not solved_cell(solving_puzzle, y, col):
                                    if solving_puzzle[row][col][1] in solving_puzzle[y][col]:
                                        if hints:
                                            return 'There is a Naked Pair in Column ' + str(col + 1)
                                        else:
                                            solving_puzzle[y][col].remove(solving_puzzle[row][col][1])
                                            progress = True
                                            solved_cell(solving_puzzle, y, col)
                        if progress:
                            # clean up with easier techniques before continuing
                            return True

                    # look in block for an identical pair
                    pairs = 1
                    yi, xi = get_upper_left(row, col)
                    for y in range(yi, yi + 3):
                        for x in range(xi, xi + 3):
                            if not (y == row and x == col) and solving_puzzle[row][col] == solving_puzzle[y][x]:
                                pairs += 1
                                row2 = copy.copy(y)
                                col2 = copy.copy(x)
                    if pairs == 2:
                        for y in range(yi, yi + 3):
                            for x in range(xi, xi + 3):
                                if not (x == col and y == row) and not (x == col2 and y == row2) and isinstance(
                                        solving_puzzle[y][x], list):
                                    if solving_puzzle[row][col][0] in solving_puzzle[y][x]:
                                        if hints:
                                            return 'There is a Naked Pair in Block ' + str(get_block(y, x) + 1)
                                        else:
                                            solving_puzzle[y][x].remove(solving_puzzle[row][col][0])
                                            progress = True
                                    if not solved_cell(solving_puzzle, y, x):
                                        if solving_puzzle[row][col][1] in solving_puzzle[y][x]:
                                            if hints:
                                                return 'There is a Naked Pair in Block ' + str(get_block(y, x) + 1)
                                            else:
                                                solving_puzzle[y][x].remove(solving_puzzle[row][col][1])
                                                progress = True
                                                solved_cell(solving_puzzle, y, x)
    return progress


def omission(solving_puzzle, hints=False):
    """If the only cells in a row for a given number lie in the same block,
    all other cells in the block must not contain that number"""
    # Written by Christopher Breen for Sprint 1, last updated July 2, 2020 for Sprint 2
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
                                    if hints:
                                        return 'Omission can be applied between Row ' + str(
                                            row + 1) + ' and Block ' + str(get_block(y, x) + 1)
                                    else:
                                        solving_puzzle[y][x].remove(num)
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
                    if x is not col:  # skip over col we found the number in
                        for y in range(by, by + 3):
                            if isinstance(solving_puzzle[y][x], list):
                                if num in solving_puzzle[y][x]:
                                    if hints:
                                        return 'Omission can be applied between Column ' + str(
                                            col + 1) + ' and Block ' + str(get_block(y, x) + 1)
                                    else:
                                        solving_puzzle[y][x].remove(num)
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
                                if hints:
                                    return 'Omission can be applied between Row ' + str(
                                        row + 1) + ' and Block ' + str(get_block(row, x) + 1)
                                else:
                                    solving_puzzle[row][x].remove(num)
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
                                if hints:
                                    return 'Omission can be applied between Column ' + str(
                                        col + 1) + ' and Block ' + str(get_block(y, col) + 1)
                                else:
                                    solving_puzzle[y][col].remove(num)
                                    progress = True
                                    if solved_cell(solving_puzzle, y, col):
                                        return progress
    return progress


def naked_triplet(solving_puzzle, hints=False):
    """Naked Triplet looks for three candidates who must exist in one of three cells.
    These numbers can be removed from any other cell in the col, row, or block."""
    # Written by Christopher Breen for Sprint 1, last updated July 3, 2020 for Sprint 2
    progress = False
    cols = set()
    candidates = set()
    for row in range(9):
        for i in range(9):
            for j in range(i + 1, 9):
                for k in range(j + 1, 9):
                    valid_set_cols = True
                    candidates.clear()
                    cols.clear()
                    for n in [i, j, k]:
                        cols.add(n)
                        if isinstance(solving_puzzle[row][n], list):
                            for digit in solving_puzzle[row][n]:
                                candidates.add(digit)
                        else:
                            # one of our three is already solved
                            valid_set_cols = False

                    if valid_set_cols and len(candidates) == 3:
                        # we have three cells with only 3 candidates
                        for x in range(9):
                            if x not in cols:
                                for digit in candidates:
                                    if isinstance(solving_puzzle[row][x], list) and digit in solving_puzzle[row][x]:
                                        if not solved_cell(solving_puzzle, row, x):
                                            if hints:
                                                return 'There is a Naked Triplet in Row ' + str(row + 1)
                                            else:
                                                solving_puzzle[row][x].remove(digit)
                                                solved_cell(solving_puzzle, row, x)
                                                progress = True
    if progress:
        return progress

    # columns
    rows = set()
    candidates = set()
    for col in range(9):
        for i in range(9):
            for j in range(i + 1, 9):
                for k in range(j + 1, 9):
                    valid_set_rows = True
                    candidates.clear()
                    rows.clear()
                    for n in [i, j, k]:
                        rows.add(n)
                        if isinstance(solving_puzzle[n][col], list):
                            for digit in solving_puzzle[n][col]:
                                candidates.add(digit)
                        else:
                            # one of our three is already solved
                            valid_set_rows = False

                    if valid_set_rows and len(candidates) == 3:
                        # we have three cells with only 3 candidates
                        for y in range(9):
                            if y not in rows:
                                for digit in candidates:
                                    if isinstance(solving_puzzle[y][col], list) and digit in solving_puzzle[y][col]:
                                        if not solved_cell(solving_puzzle, y, col):
                                            if hints:
                                                return 'There is a Naked Triplet in Column ' + str(col + 1)
                                            else:
                                                solving_puzzle[y][col].remove(digit)
                                                solved_cell(solving_puzzle, y, col)
                                                progress = True
    if progress:
        return progress

    # blocks
    locations = set()
    candidates = set()
    for block in range(9):
        for i in range(9):
            for j in range(i + 1, 9):
                for k in range(j + 1, 9):
                    valid_set = True
                    candidates.clear()
                    locations.clear()
                    for n in [i, j, k]:
                        row, col = block_to_coords(block, n)
                        locations.add(str(row) + (str(col)))
                        if isinstance(solving_puzzle[row][col], list):
                            for digit in solving_puzzle[row][col]:
                                candidates.add(digit)
                        else:
                            # one of our three is already solved
                            valid_set = False

                    if valid_set and len(candidates) == 3:
                        # we have three cells with only 3 candidates
                        yi, xi = block_to_coords(block, 0)
                        for y in range(yi, yi + 3):
                            for x in range(xi, xi + 3):
                                if (str(y) + str(x)) not in locations:
                                    for digit in candidates:
                                        if isinstance(solving_puzzle[y][x], list) and digit in solving_puzzle[y][x]:
                                            if not solved_cell(solving_puzzle, y, x):
                                                if hints:
                                                    return 'There is a Naked Triplet in Block ' + get_block(y, x) + 1
                                                else:
                                                    solving_puzzle[y][x].remove(digit)
                                                    solved_cell(solving_puzzle, y, x)
                                                    progress = True
    return progress


def hidden_pair(solving_puzzle, hints=False):
    """Two cells in same row/col/block that contain the only two locations for two numbers indicates those same two
    cells must not contain any of the other remaining candidates"""
    # Written by Christopher Breen for Sprint 2, last updated June 28, 2020

    # scan row
    progress = False
    for row in range(9):
        # digit locs len(10) to skip index 0
        digit_locations = [[], [], [], [], [], [], [], [], [], []]
        for digit in range(1, 10):
            for col in range(9):
                if isinstance(solving_puzzle[row][col], list):
                    if digit in solving_puzzle[row][col]:
                        # add col digit appears in
                        digit_locations[digit].append(col)
        # finished with the row, look for 2 digits that only exist in same 2 cells
        for i in range(1, 10):
            for j in range(1, 10):
                if i != j and digit_locations[i] == digit_locations[j]:
                    if len(digit_locations[i]) == 2:
                        col1 = digit_locations[i][0]
                        col2 = digit_locations[i][1]
                        if len(solving_puzzle[row][col1]) > 2:
                            if hints:
                                return 'There is a Hidden Pair in Row ' + str(row + 1)
                            else:
                                solving_puzzle[row][col1] = [i, j]
                                progress = True
                        if len(solving_puzzle[row][col2]) > 2:
                            if hints:
                                return 'There is a Hidden Pair in Row ' + str(row + 1)
                            else:
                                solving_puzzle[row][col2] = [i, j]
                                progress = True
                        if progress:
                            return progress
        digit_locations.clear()

    # scan col
    progress = False
    for col in range(9):
        digit_locations = [[], [], [], [], [], [], [], [], [], []]
        for digit in range(1, 10):
            digit_solved = False
            for row in range(9):
                if isinstance(solving_puzzle[row][col], list):
                    if digit in solving_puzzle[row][col]:
                        # keep track of each location for each digit
                        digit_locations[digit].append(row)
        # finished with the col, look for 2 digits that only exist in same 2 cells
        for i in range(1, 10):
            for j in range(1, 10):
                if i != j and digit_locations[i] == digit_locations[j]:
                    if len(digit_locations[i]) == 2:
                        row1 = digit_locations[i][0]
                        row2 = digit_locations[i][1]
                        if len(solving_puzzle[row1][col]) > 2:
                            if hints:
                                return 'There is a Hidden Pair in Column ' + str(col + 1)
                            else:
                                solving_puzzle[row1][col] = [i, j]
                                progress = True
                        if len(solving_puzzle[row2][col]) > 2:
                            if hints:
                                return 'There is a Hidden Pair in Column ' + str(col + 1)
                            else:
                                solving_puzzle[row2][col] = [i, j]
                                progress = True
                        if progress:
                            return progress
        digit_locations.clear()

    # scan block
    progress = False
    for block in range(9):
        by = math.floor(block / 3) * 3
        bx = (block % 3) * 3
        digit_locations = [[], [], [], [], [], [], [], [], [], []]
        for digit in range(1, 10):
            for row in range(by, by + 3):
                for col in range(bx, bx + 3):
                    if isinstance(solving_puzzle[row][col], list):
                        if digit in solving_puzzle[row][col]:
                            # keep track of each location for each digit
                            digit_locations[digit].append((row, col))

        # finished with the block, look for 2 digits that only exist in same 2 cells
        for i in range(1, 10):
            for j in range(1, 10):
                if i != j and digit_locations[i] == digit_locations[j]:
                    if len(digit_locations[i]) == 2:
                        row1 = digit_locations[i][0][0]
                        col1 = digit_locations[i][0][1]
                        row2 = digit_locations[i][1][0]
                        col2 = digit_locations[i][1][1]
                        if len(solving_puzzle[row1][col1]) > 2:
                            if hints:
                                return 'There is a Hidden Pair in Block ' + str(get_block(row1, col1) + 1)
                            else:
                                solving_puzzle[row1][col1] = [i, j]
                                progress = True
                        if len(solving_puzzle[row2][col2]) > 2:
                            if hints:
                                return 'There is a Hidden Pair in Block ' + str(get_block(row2, col2) + 1)
                            else:
                                solving_puzzle[row2][col2] = [i, j]
                                progress = True
                        if progress:
                            return progress
        digit_locations.clear()

    return progress


def naked_quad(solving_puzzle, hints=False):
    """Naked Quad looks for four candidates who must exist in one of four cells.
    These numbers can be removed from any other cell in the col, row, or block."""
    # Written by Christopher Breen for Sprint 2, last updated July 3, 2020
    progress = False
    cols = set()
    candidates = set()
    for row in range(9):
        for i in range(9):
            for j in range(i + 1, 9):
                for k in range(j + 1, 9):
                    for m in range(k + 1, 9):
                        valid_set_cols = True
                        candidates.clear()
                        cols.clear()
                        for n in [i, j, k, m]:
                            cols.add(n)
                            if isinstance(solving_puzzle[row][n], list):
                                for digit in solving_puzzle[row][n]:
                                    candidates.add(digit)
                            else:
                                # one of our four is already solved
                                valid_set_cols = False

                        if valid_set_cols and len(candidates) == 4:
                            # we have four cells with only 4 candidates
                            for x in range(9):
                                if x not in cols:
                                    for digit in candidates:
                                        if isinstance(solving_puzzle[row][x], list) and digit in solving_puzzle[row][x]:
                                            if not solved_cell(solving_puzzle, row, x):
                                                if hints:
                                                    return 'There is a Naked Quad in Row ' + str(row + 1)
                                                else:
                                                    solving_puzzle[row][x].remove(digit)
                                                    solved_cell(solving_puzzle, row, x)
                                                    progress = True
    if progress:
        return progress

    # columns
    rows = set()
    candidates = set()
    for col in range(9):
        for i in range(9):
            for j in range(i + 1, 9):
                for k in range(j + 1, 9):
                    for m in range(k + 1, 9):
                        valid_set_rows = True
                        candidates.clear()
                        rows.clear()
                        for n in [i, j, k, m]:
                            rows.add(n)
                            if isinstance(solving_puzzle[n][col], list):
                                for digit in solving_puzzle[n][col]:
                                    candidates.add(digit)
                            else:
                                # one of our four is already solved
                                valid_set_rows = False

                        if valid_set_rows and len(candidates) == 4:
                            # we have four cells with only 4 candidates
                            for y in range(9):
                                if y not in rows:
                                    for digit in candidates:
                                        if isinstance(solving_puzzle[y][col], list) and digit in solving_puzzle[y][col]:
                                            if not solved_cell(solving_puzzle, y, col):
                                                if hints:
                                                    return 'There is a Naked Quad in Column ' + str(col + 1)
                                                else:
                                                    solving_puzzle[y][col].remove(digit)
                                                    solved_cell(solving_puzzle, y, col)
                                                    progress = True
    if progress:
        return progress

    # blocks
    locations = set()
    candidates = set()
    for block in range(9):
        for i in range(9):
            for j in range(i + 1, 9):
                for k in range(j + 1, 9):
                    for m in range(k + 1, 9):
                        valid_set = True
                        candidates.clear()
                        locations.clear()
                        for n in [i, j, k, m]:
                            row, col = block_to_coords(block, n)
                            locations.add(str(row) + (str(col)))
                            if isinstance(solving_puzzle[row][col], list):
                                for digit in solving_puzzle[row][col]:
                                    candidates.add(digit)
                            else:
                                # one of our four is already solved
                                valid_set = False

                        if valid_set and len(candidates) == 4:
                            # we have four cells with only 4 candidates
                            yi, xi = block_to_coords(block, 0)
                            for y in range(yi, yi + 3):
                                for x in range(xi, xi + 3):
                                    if (str(y) + str(x)) not in locations:
                                        for digit in candidates:
                                            if isinstance(solving_puzzle[y][x], list) and digit in solving_puzzle[y][x]:
                                                if not solved_cell(solving_puzzle, y, x):
                                                    if hints:
                                                        return 'There is a Naked Quad in Block ' + get_block(y, x) + 1
                                                    else:
                                                        solving_puzzle[y][x].remove(digit)
                                                        solved_cell(solving_puzzle, y, x)
                                                        progress = True
    return progress


def hidden_triplet(solving_puzzle, hints=False):
    """Three cells in same row/col/block that contain the only three locations for three numbers indicates those same
    three cells must not contain any of the other remaining candidates"""
    # Written by Christopher Breen for Sprint 2, last updated June 28, 2020

    # scan row
    progress = False
    for row in range(9):
        # digit locs len(10) to skip index 0
        digit_locations = [[], [], [], [], [], [], [], [], [], []]
        for digit in range(1, 10):
            for col in range(9):
                if isinstance(solving_puzzle[row][col], list):
                    if digit in solving_puzzle[row][col]:
                        # add col digit appears in
                        digit_locations[digit].append(col)
        # finished with the row, look for 3 digits that only exist in same 3 cells
        for i in range(1, 10):
            for j in range(1, 10):
                for k in range(1, 10):
                    if i != j and j != k and i != k and digit_locations[i] == digit_locations[j] == digit_locations[k]:
                        if len(digit_locations[i]) == 3:
                            col1 = digit_locations[i][0]
                            col2 = digit_locations[i][1]
                            col3 = digit_locations[i][2]
                            if len(solving_puzzle[row][col1]) > 3:
                                if hints:
                                    return 'There is a Hidden Triplet in Row ' + str(row + 1)
                                else:
                                    solving_puzzle[row][col1] = [i, j, k]
                                    progress = True
                            if len(solving_puzzle[row][col2]) > 3:
                                if hints:
                                    return 'There is a Hidden Triplet in Row ' + str(row + 1)
                                else:
                                    solving_puzzle[row][col2] = [i, j, k]
                                    progress = True
                            if len(solving_puzzle[row][col3]) > 3:
                                if hints:
                                    return 'There is a Hidden Triplet in Row ' + str(row + 1)
                                else:
                                    solving_puzzle[row][col3] = [i, j, k]
                                    progress = True
                            if progress:
                                return progress
        digit_locations.clear()

    # scan col
    progress = False
    for col in range(9):
        digit_locations = [[], [], [], [], [], [], [], [], [], []]
        for digit in range(1, 10):
            for row in range(9):
                if isinstance(solving_puzzle[row][col], list):
                    if digit in solving_puzzle[row][col]:
                        # keep track of each location for each digit
                        digit_locations[digit].append(row)
        # finished with the col, look for 3 digits that only exist in same 3 cells
        for i in range(1, 10):
            for j in range(1, 10):
                for k in range(1, 10):
                    if i != j and i != k and j != k and digit_locations[i] == digit_locations[j] == digit_locations[k]:
                        if len(digit_locations[i]) == 3:
                            row1 = digit_locations[i][0]
                            row2 = digit_locations[i][1]
                            row3 = digit_locations[i][2]
                            if len(solving_puzzle[row1][col]) > 3:
                                if hints:
                                    return 'There is a Hidden Triplet in Column ' + str(col + 1)
                                else:
                                    solving_puzzle[row1][col] = [i, j, k]
                                    progress = True
                            if len(solving_puzzle[row2][col]) > 3:
                                if hints:
                                    return 'There is a Hidden Triplet in Column ' + str(col + 1)
                                else:
                                    solving_puzzle[row2][col] = [i, j, k]
                                    progress = True
                            if len(solving_puzzle[row3][col]) > 3:
                                if hints:
                                    return 'There is a Hidden Triplet in Column ' + str(col + 1)
                                else:
                                    solving_puzzle[row3][col] = [i, j, k]
                                    progress = True
                            if progress:
                                return progress
        digit_locations.clear()

    # scan block
    progress = False
    for block in range(9):
        by = math.floor(block / 3) * 3
        bx = (block % 3) * 3
        digit_locations = [[], [], [], [], [], [], [], [], [], []]
        for digit in range(1, 10):
            for row in range(by, by + 3):
                for col in range(bx, bx + 3):
                    if isinstance(solving_puzzle[row][col], list):
                        if digit in solving_puzzle[row][col]:
                            # keep track of each location for each digit
                            digit_locations[digit].append((row, col))

        # finished with the block, look for 3 digits that only exist in same 3 cells
        for i in range(1, 10):
            for j in range(1, 10):
                for k in range(1, 10):
                    if i != j and i != k and j != k and digit_locations[i] == digit_locations[j] == digit_locations[k]:
                        if len(digit_locations[i]) == 3:
                            row1 = digit_locations[i][0][0]
                            col1 = digit_locations[i][0][1]
                            row2 = digit_locations[i][1][0]
                            col2 = digit_locations[i][1][1]
                            row3 = digit_locations[i][2][0]
                            col3 = digit_locations[i][2][1]
                            if len(solving_puzzle[row1][col1]) > 3:
                                if hints:
                                    return 'There is a Hidden Triplet in Block ' + str(get_block(row1, col1) + 1)
                                else:
                                    solving_puzzle[row1][col1] = [i, j, k]
                                    progress = True
                            if len(solving_puzzle[row2][col2]) > 3:
                                if hints:
                                    return 'There is a Hidden Triplet in Block ' + str(get_block(row1, col1) + 1)
                                else:
                                    solving_puzzle[row2][col2] = [i, j, k]
                                    progress = True
                            if len(solving_puzzle[row3][col3]) > 3:
                                if hints:
                                    return 'There is a Hidden Triplet in Block ' + str(get_block(row1, col1) + 1)
                                else:
                                    solving_puzzle[row3][col3] = [i, j, k]
                                    progress = True
                            if progress:
                                return progress
        digit_locations.clear()

    return progress


def hidden_quad(solving_puzzle, hints=False):
    """Four cells in same row/col/block that contain the only four locations for four numbers indicates those same
    four cells must not contain any of the other remaining candidates"""
    # Written by Christopher Breen for Sprint 3, last updated July 2, 2020

    # scan row
    progress = False
    for row in range(9):
        # digit locs len(10) to skip index 0
        digit_locations = [[], [], [], [], [], [], [], [], [], []]
        for digit in range(1, 10):
            for col in range(9):
                if isinstance(solving_puzzle[row][col], list):
                    if digit in solving_puzzle[row][col]:
                        # add col digit appears in
                        digit_locations[digit].append(col)
        # finished with the row, look for 4 digits that only exist in same 4 cells
        for i in range(1, 10):
            for j in range(i + 1, 10):
                for k in range(j + 1, 10):
                    for m in range(k + 1, 10):
                        if i != j and i != k and i != m and j != k and j != m and k != m and \
                                digit_locations[i] == digit_locations[j] == digit_locations[k] == digit_locations[m]:
                            if len(digit_locations[i]) == 4:
                                col1 = digit_locations[i][0]
                                col2 = digit_locations[i][1]
                                col3 = digit_locations[i][2]
                                col4 = digit_locations[i][3]
                                if len(solving_puzzle[row][col1]) > 4:
                                    if hints:
                                        return 'There is a Hidden Quad in Row ' + str(row + 1)
                                    else:
                                        solving_puzzle[row][col1] = [i, j, k, m]
                                        print('HQ', end='')
                                        progress = True
                                if len(solving_puzzle[row][col2]) > 4:
                                    if hints:
                                        return 'There is a Hidden Quad in Row ' + str(row + 1)
                                    else:
                                        solving_puzzle[row][col2] = [i, j, k, m]
                                        print('HQ', end='')
                                        progress = True
                                if len(solving_puzzle[row][col3]) > 4:
                                    if hints:
                                        return 'There is a Hidden Quad in Row ' + str(row + 1)
                                    else:
                                        solving_puzzle[row][col3] = [i, j, k, m]
                                        print('HQ', end='')
                                        progress = True
                                if len(solving_puzzle[row][col4]) > 4:
                                    if hints:
                                        return 'There is a Hidden Quad in Row ' + str(row + 1)
                                    else:
                                        solving_puzzle[row][col4] = [i, j, k, m]
                                        print('HQ', end='')
                                        progress = True
                                if progress:
                                    return progress
        digit_locations.clear()

    # scan col
    progress = False
    for col in range(9):
        digit_locations = [[], [], [], [], [], [], [], [], [], []]
        for digit in range(1, 10):
            for row in range(9):
                if isinstance(solving_puzzle[row][col], list):
                    if digit in solving_puzzle[row][col]:
                        # keep track of each location for each digit
                        digit_locations[digit].append(row)
        # finished with the col, look for 4 digits that only exist in same 4 cells
        for i in range(1, 10):
            for j in range(i + 1, 10):
                for k in range(j + 1, 10):
                    for m in range(k + 1, 10):
                        if i != j and i != k and i != m and j != k and j != m and k != m and \
                                digit_locations[i] == digit_locations[j] == digit_locations[k] == digit_locations[m]:
                            if len(digit_locations[i]) == 4:
                                row1 = digit_locations[i][0]
                                row2 = digit_locations[i][1]
                                row3 = digit_locations[i][2]
                                row4 = digit_locations[i][3]
                                if len(solving_puzzle[row1][col]) > 4:
                                    if hints:
                                        return 'There is a Hidden Quad in Column ' + str(col + 1)
                                    else:
                                        solving_puzzle[row1][col] = [i, j, k, m]
                                        print('HQ', end='')
                                        progress = True
                                if len(solving_puzzle[row2][col]) > 4:
                                    if hints:
                                        return 'There is a Hidden Quad in Column ' + str(col + 1)
                                    else:
                                        solving_puzzle[row2][col] = [i, j, k, m]
                                        print('HQ', end='')
                                        progress = True
                                if len(solving_puzzle[row3][col]) > 4:
                                    if hints:
                                        return 'There is a Hidden Quad in Column ' + str(col + 1)
                                    else:
                                        solving_puzzle[row3][col] = [i, j, k, m]
                                        print('HQ', end='')
                                        progress = True
                                if len(solving_puzzle[row4][col]) > 4:
                                    if hints:
                                        return 'There is a Hidden Quad in Column ' + str(col + 1)
                                    else:
                                        solving_puzzle[row3][col] = [i, j, k, m]
                                        print('HQ', end='')
                                        progress = True
                                if progress:
                                    return progress
        digit_locations.clear()

    # scan block
    progress = False
    for block in range(9):
        by = math.floor(block / 3) * 3
        bx = (block % 3) * 3
        digit_locations = [[], [], [], [], [], [], [], [], [], []]
        for digit in range(1, 10):
            for row in range(by, by + 3):
                for col in range(bx, bx + 3):
                    if isinstance(solving_puzzle[row][col], list):
                        if digit in solving_puzzle[row][col]:
                            # keep track of each location for each digit
                            digit_locations[digit].append((row, col))

        # finished with the block, look for 3 digits that only exist in same 3 cells
        for i in range(1, 10):
            for j in range(i + 1, 10):
                for k in range(j + 1, 10):
                    for m in range(k + 1, 10):
                        if i != j and i != k and i != m and j != k and j != m and k != m and \
                                digit_locations[i] == digit_locations[j] == digit_locations[k] == digit_locations[m]:
                            if len(digit_locations[i]) == 4:
                                row1 = digit_locations[i][0][0]
                                col1 = digit_locations[i][0][1]
                                row2 = digit_locations[i][1][0]
                                col2 = digit_locations[i][1][1]
                                row3 = digit_locations[i][2][0]
                                col3 = digit_locations[i][2][1]
                                row4 = digit_locations[i][3][0]
                                col4 = digit_locations[i][3][1]
                                if len(solving_puzzle[row1][col1]) > 4:
                                    if hints:
                                        return 'There is a Hidden Quad in Block ' + str(get_block(row1, col1) + 1)
                                    else:
                                        solving_puzzle[row1][col1] = [i, j, k, m]
                                        print('HQ', end='')
                                        progress = True
                                if len(solving_puzzle[row2][col2]) > 4:
                                    if hints:
                                        return 'There is a Hidden Quad in Block ' + str(get_block(row2, col2) + 1)
                                    else:
                                        solving_puzzle[row2][col2] = [i, j, k, m]
                                        print('HQ', end='')
                                        progress = True
                                if len(solving_puzzle[row3][col3]) > 4:
                                    if hints:
                                        return 'There is a Hidden Quad in Block ' + str(get_block(row3, col3) + 1)
                                    else:
                                        solving_puzzle[row3][col3] = [i, j, k, m]
                                        print('HQ', end='')
                                        progress = True
                                if len(solving_puzzle[row4][col4]) > 4:
                                    if hints:
                                        return 'There is a Hidden Quad in Block ' + str(get_block(row4, col4) + 1)
                                    else:
                                        solving_puzzle[row4][col4] = [i, j, k, m]
                                        print('HQ', end='')
                                        progress = True
                                if progress:
                                    return progress
        digit_locations.clear()

    return progress


def block_to_coords(block, sequence):
    """Receives block number 1 through 9 and sequence 1 through 9, both read left to right, top to bottom, and
    returns the y, x coordinates on the puzzle"""
    #     0 1 2 3 4 5 6 7 8
    #     - - - - - - - - -
    # 0 - 0 1 2 0 1 2 0 1 2
    # 1 - 3 4 5 3 4 5 3 4 5
    # 2 - 6 7 8 6 7 8 6 7 8
    # 3 - 0 1 2 0 1 2 0 1 2
    # 4 - 3 4 5 3 4 5 3 4 5
    # 5 - 6 7 8 6 7 8 6 7 8
    # 6 - 0 1 2 0 1 2 0 1 2
    # 7 - 3 4 5 3 4 5 3 4 5
    # 8 - 6 7 8 6 7 8 6 7 8
    y = (math.floor(block / 3) * 3) + (math.floor(sequence / 3))
    x = ((block % 3) * 3) + (sequence % 3)
    return y, x


def get_upper_left(row, col):
    """Returns row and col of upper left cell in block"""
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
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
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
    for row in range(9):
        for col in range(9):
            if isinstance(puzzle[row][col], list):
                return False
    return True


def solved_cell(solving_puzzle, y, x):
    # we removed a number from the scratchpad.
    # if there is only one number remaining we must convert type of cell from list of length one into an integer
    # otherwise we run into problems in various techniques looking for cells with multiple options remaining
    # Written by Christopher Breen for Sprint 1, last updated June 23, 2020
    if len(solving_puzzle[y][x]) == 1:
        solving_puzzle[y][x] = solving_puzzle[y][x][0]
        return True
    return False
