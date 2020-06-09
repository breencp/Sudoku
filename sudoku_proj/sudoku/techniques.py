# file: techniques.py
# author: Christopher Breen
# date:
import copy


def solvable_puzzle(puzzle_to_solve, desired_difficulty):
    """Returns true if able to solve provided puzzle with provided difficulty level"""
    progress = True
    techniques_utilized = set()
    actual_difficulty = '1'
    while progress:
        progress = False
        # Naked Single: only technique that solves more than one within function
        if naked_single(puzzle_to_solve):
            techniques_utilized.add("Naked Single")
            progress = True
        # Hidden Single
        if hidden_single(puzzle_to_solve):
            techniques_utilized.add("Hidden Single")
            progress = True
        if desired_difficulty > '1':
            # Naked Pair: repeatedly try easier techniques until no longer making progress without advanced techniques
            if not progress:
                if naked_pair(puzzle_to_solve):
                    techniques_utilized.add("Naked Pair")
                    if actual_difficulty < '2':
                        actual_difficulty = '2'
                    progress = True
            # Omission (a.k.a. Intersection, Pointing)
            if not progress:
                if omission(puzzle_to_solve):
                    techniques_utilized.add("Omission")
                    if actual_difficulty < '2':
                        actual_difficulty = '2'
            # Naked Triplet
        if desired_difficulty > '2':
            # Hidden Pair
            # Naked Quad
            # Hidden Triplet
            pass
        if desired_difficulty > '3':
            # Hidden Quad
            # X-Wing
            # Swordfish
            # XY-Wing
            # Unique Rectangle
            pass

    # debug specific technique TODO: remove from production code
    #if 'Naked Pair' not in techniques_utilized:
    #    # keep going until we solve a puzzle using the technique we are testing
    #    print('*', end='')
    #    return False

    # we have continually looped through all techniques in the given difficulty level
    # we may or may not have removed all available numbers down to a single int.  Let's check.
    # if is_solved(puzzle_to_solve):  # test code, replace with line below
    if is_solved(puzzle_to_solve):
        print("\nTechniques: " + str(techniques_utilized), end='')
        if actual_difficulty == desired_difficulty:
            return True
        else:
            return False
    else:
        return False


def naked_single(solving_puzzle):
    """Naked Single removes any number found in the current row, col, and block.  If only one single number remains,
    it is the solution to that cell"""
    solved_one = False
    progress = True
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
                            solved_one = True
                            # print([row][0]), [col][0], solving_puzzle[row][col]
                    clean_cell(solving_puzzle, row, col)

    return solved_one


def hidden_single(solving_puzzle):
    """Hidden single looks at the pencil marks in each cell and then each cell within the row/col/block to
    see if it contains a number that is not contained in pencil marks of any other cell in the row/col/block"""
    single = True
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
    pairs = 0
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
                                    if not clean_cell(solving_puzzle, row, x):
                                        if solving_puzzle[row][col][1] in solving_puzzle[row][x]:
                                            solving_puzzle[row][x].remove(solving_puzzle[row][col][1])
                                            clean_cell(solving_puzzle, row, x)
                                            progress = True
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
                                            if not clean_cell(solving_puzzle, y, x):
                                                if solving_puzzle[row][col][1] in solving_puzzle[y][x]:
                                                    solving_puzzle[y][x].remove(solving_puzzle[row][col][1])
                                                    clean_cell(solving_puzzle, y, x)
                                                    progress = True
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
                                    if not clean_cell(solving_puzzle, y, col):
                                        if solving_puzzle[row][col][1] in solving_puzzle[y][col]:
                                            solving_puzzle[y][col].remove(solving_puzzle[row][col][1])
                                            clean_cell(solving_puzzle, y, col)
                                            progress = True
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
                                            if not clean_cell(solving_puzzle, y, x):
                                                if solving_puzzle[row][col][1] in solving_puzzle[y][x]:
                                                    solving_puzzle[y][x].remove(solving_puzzle[row][col][1])
                                                    clean_cell(solving_puzzle, y, x)
                                                    progress = True

    return progress


def omission(solving_puzzle):

    return False


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


def clean_cell(solving_puzzle, y, x):
    if len(solving_puzzle[y][x]) == 1:
        solving_puzzle[y][x] = solving_puzzle[y][x][0]
        return True
    return False
