# file: techniques.py
# author: Christopher Breen
# date:
import copy
import math


def solvable_puzzle(puzzle_to_solve, hints=False):
    """Returns true if able to solve provided puzzle with provided difficulty level"""
    progress = True
    techniques_utilized = dict()
    actual_difficulty = '1'
    while progress:
        progress = False

        # Difficulty Level 1
        # Naked Single: only technique that solves more than one within function
        if naked_single(puzzle_to_solve, hints):
            techniques_utilized.update({'naked_single': 'True'})
            progress = True
        # Hidden Single
        if hidden_single(puzzle_to_solve, hints):
            techniques_utilized.update({'hidden_single': 'True'})
            progress = True

        # Difficulty Level 2
        # Naked Pair: repeatedly try easier techniques until no longer making progress without advanced techniques
        if not progress:
            if naked_pair(puzzle_to_solve, hints):
                techniques_utilized.update({'naked_pair': 'True'})
                if actual_difficulty < '2':
                    actual_difficulty = '2'
                progress = True
        # Omission (a.k.a. Intersection, Pointing)
        if not progress:
            if omission(puzzle_to_solve, hints):
                techniques_utilized.update({'omission': 'True'})
                if actual_difficulty < '2':
                    actual_difficulty = '2'
                progress = True
        # Naked Triplet
        if not progress:
            if naked_triplet(puzzle_to_solve, hints):
                techniques_utilized.update({'naked_triplet': 'True'})
                if actual_difficulty < '2':
                    actual_difficulty = '2'
                progress = True

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


def naked_single(solving_puzzle, hints=False):
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
                            if hints:
                                print('Naked Single:', digit, 'removed from', row, col)
                    if solved_cell(solving_puzzle, row, col):
                        # other techniques need to be exited to allow cleanup by naked_single
                        pass
    return overall_progress


def hidden_single(solving_puzzle, hints=False):
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


def naked_pair(solving_puzzle, hints=False):
    """Naked Pair looks for two cells with an identical pair of remaining numbers.
    These numbers can be removed from any other cell in the col, row, or block."""
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
                                    solving_puzzle[row][x].remove(solving_puzzle[row][col][0])
                                    progress = True
                                if not solved_cell(solving_puzzle, row, x):
                                    if solving_puzzle[row][col][1] in solving_puzzle[row][x]:
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
                                    solving_puzzle[y][col].remove(solving_puzzle[row][col][0])
                                    progress = True
                                if not solved_cell(solving_puzzle, y, col):
                                    if solving_puzzle[row][col][1] in solving_puzzle[y][col]:
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
                                        solving_puzzle[y][x].remove(solving_puzzle[row][col][0])
                                        progress = True
                                    if not solved_cell(solving_puzzle, y, x):
                                        if solving_puzzle[row][col][1] in solving_puzzle[y][x]:
                                            solving_puzzle[y][x].remove(solving_puzzle[row][col][1])
                                            progress = True
                                            solved_cell(solving_puzzle, y, x)
    return progress


def omission(solving_puzzle, hints=False):
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


def naked_triplet(solving_puzzle, hints=False):
    """Naked Triplet looks for three cells with an identical three candidates.
    These numbers can be removed from any other cell in the col, row, or block."""
    progress = False
    cols = set()
    candidates = set()
    for row in range(9):
        for i in range(7, 448):  # range within 512 we are interested in
            # looking for all possible combinations of 3 cells in a given row
            candidates.clear()
            cols.clear()
            valid_set_cols = True
            if num_set_bits(i) == 3:
                for b in bits(i):
                    col = get_location_from_bits(b)
                    cols.add(col)
                    if isinstance(solving_puzzle[row][col], list):
                        for digit in solving_puzzle[row][col]:
                            candidates.add(digit)
                    else:
                        # one of our three is already solved, move on
                        valid_set_cols = False
                if valid_set_cols and len(candidates) == 3:
                    # we have three cells with only 3 candidates
                    for x in range(9):
                        if x not in cols:
                            for digit in candidates:
                                if isinstance(solving_puzzle[row][x], list) and digit in solving_puzzle[row][x]:
                                    if not solved_cell(solving_puzzle, row, x):
                                        solving_puzzle[row][x].remove(digit)
                                        solved_cell(solving_puzzle, row, x)
                                        progress = True
    if progress:
        return progress

    # scan columns
    progress = False
    rows = set()
    candidates = set()
    for col in range(9):
        for i in range(7, 448):  # range within 512 we are interested in
            # looking for all possible combinations of 3 cells in a given col
            candidates.clear()
            rows.clear()
            valid_set_rows = True
            if num_set_bits(i) == 3:
                for b in bits(i):
                    row = get_location_from_bits(b)
                    rows.add(row)
                    if isinstance(solving_puzzle[row][col], list):
                        for digit in solving_puzzle[row][col]:
                            candidates.add(digit)
                    else:
                        # one of our three is already solved, move on
                        valid_set_rows = False
                if valid_set_rows and len(candidates) == 3:
                    # we have three cells with only 3 candidates
                    for y in range(9):
                        if y not in rows:
                            for digit in candidates:
                                if isinstance(solving_puzzle[y][col], list) and digit in solving_puzzle[y][col]:
                                    if not solved_cell(solving_puzzle, y, col):
                                        solving_puzzle[y][col].remove(digit)
                                        solved_cell(solving_puzzle, y, col)
                                        progress = True
    if progress:
        return progress

    # scan blocks
    progress = False
    candidates = set()
    locations = set()
    for block in range(9):
        for i in range(7, 448):  # range within 512 we are interested in
            # looking for all possible combinations of 3 cells in a given block
            candidates.clear()
            locations.clear()
            valid_combo = True
            if num_set_bits(i) == 3:
                for b in bits(i):
                    row, col = get_location_from_bits(b, block)
                    locations.add(str(row) + (str(col)))
                    if isinstance(solving_puzzle[row][col], list):
                        for digit in solving_puzzle[row][col]:
                            candidates.add(digit)
                    else:
                        # one of our three is already solved, move on
                        valid_combo = False
                if valid_combo and len(candidates) == 3:
                    # we have three cells with only 3 candidates
                    yi = math.floor(block / 3) * 3
                    xi = (block % 3) * 3
                    for y in range(yi, yi + 3):
                        for x in range(xi, xi + 3):
                            if (str(y) + (str(x))) not in locations:
                                for digit in candidates:
                                    if isinstance(solving_puzzle[y][x], list) and digit in solving_puzzle[y][x]:
                                        if not solved_cell(solving_puzzle, y, x):
                                            solving_puzzle[y][x].remove(digit)
                                            solved_cell(solving_puzzle, y, x)
                                            progress = True
    return progress


def get_location_from_bits(b, block=False):
    # block 0, 1, 2: y = 0, x = 0, 3, 6
    # block 3, 4, 5: y = 3, x = 0, 3, 6
    # block 6, 7, 8: y = 6, x = 0, 3, 6
    if block is not False:
        by = math.floor(block / 3) * 3
        bx = (block % 3) * 3

        if b == 1:
            return by + 2, bx + 2
        if b == 2:
            return by + 2, bx + 1
        if b == 4:
            return by + 2, bx
        if b == 8:
            return by + 1, bx + 2
        if b == 16:
            return by + 1, bx + 1
        if b == 32:
            return by + 1, bx
        if b == 64:
            return by, bx + 2
        if b == 128:
            return by, bx + 1
        if b == 256:
            return by, bx
    else:
        if b == 1:
            return 8
        if b == 2:
            return 7
        if b == 4:
            return 6
        if b == 8:
            return 5
        if b == 16:
            return 4
        if b == 32:
            return 3
        if b == 64:
            return 2
        if b == 128:
            return 1
        if b == 256:
            return 0


def num_set_bits(n):
    # use python bitwise operators to determine combinations of three cells in a row/col
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


def bits(n):
    while n:
        b = n & (~n+1)
        yield b
        n ^= b


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
