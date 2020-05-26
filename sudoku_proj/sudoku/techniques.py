# file: techniques.py
# author: Christopher Breen
# date: May 24, 2020


def solvable_puzzle(puzzle_to_solve, difficulty):
    """Returns true if able to solve provided puzzle with provided difficulty level"""
    progress = True
    techniques_utilized = set()
    while progress:
        progress = False
        # Naked Single
        if naked_single(puzzle_to_solve):
            techniques_utilized.add("Naked Single")
            progress = True
        # Hidden Single
        if hidden_single(puzzle_to_solve):
            techniques_utilized.add("Hidden Single")
            progress = True

        if difficulty > '1':
            # Naked Pair
            # Omission
            # Naked Triplet
            pass
        if difficulty > '2':
            # Hidden Pair
            # Naked Quad
            # Hidden Triplet
            pass
        if difficulty > '3':
            # Hidden Quad
            # X-Wing
            # Swordfish
            # XY-Wing
            # Unique Rectangle
            pass

    # we have continually looped through all techniques in the given difficulty level
    # we may or may not have removed all available numbers down to a single int.  Let's check.
    if 'Hidden Single' not in techniques_utilized:
        return False

    if is_solved(puzzle_to_solve):
        print("\nTechniques: ", techniques_utilized)
        return True
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
                    xi, yi = get_upper_left(row, col)
                    for y in range(yi, yi + 3):
                        for x in range(xi, xi + 3):
                            if not (x is col and y is row) and not isinstance(solving_puzzle[y][x], list):
                                nums_used.add(solving_puzzle[y][x])
                    for digit in nums_used:
                        if digit in solving_puzzle[row][col]:
                            solving_puzzle[row][col].remove(digit)
                            progress = True
                            solved_one = True
                    if len(solving_puzzle[row][col]) == 1:
                        # single digit remaining, replace list with integer
                        solving_puzzle[row][col] = solving_puzzle[row][col][0]
    return solved_one


def hidden_single(solving_puzzle):
    """Hidden single looks at the pencil marks in each cell and then each cell within the row/col/block to
    see if it contains a number that is not contained in pencil marks of any other cell in the row/col/block"""
    progress = True
    solved_one = False
    while progress:
        progress = False
        for row in range(9):
            for col in range(9):
                if isinstance(solving_puzzle[row][col], list):
                    # this is an unsolved cell
                    cell_possibles = solving_puzzle[row][col][:]
                    for x in range(9):
                        if x is not col and isinstance(solving_puzzle[row][x], list):
                            for digit in solving_puzzle[row][x]:
                                if digit in cell_possibles:
                                    cell_possibles.remove(digit)
                                    if len(cell_possibles) == 0:
                                        break
                    if len(cell_possibles) == 1:
                        # we have a hidden single
                        progress = True
                        solved_one = True
                        solving_puzzle[row][col] = cell_possibles[0]

                    if isinstance(solving_puzzle[row][col], list):
                        cell_possibles = solving_puzzle[row][col][:]
                        for y in range(9):
                            if y is not row and isinstance(solving_puzzle[y][col], list):
                                for digit in solving_puzzle[y][col]:
                                    if digit in cell_possibles:
                                        cell_possibles.remove(digit)
                        if len(cell_possibles) == 1:
                            # we have a hidden single
                            progress = True
                            solved_one = True
                            solving_puzzle[row][col] = cell_possibles[0]

                    if isinstance(solving_puzzle[row][col], list):
                        cell_possibles = solving_puzzle[row][col][:]
                        xi, yi = get_upper_left(row, col)
                        for y in range(yi, yi + 3):
                            for x in range(xi, xi + 3):
                                if not (x is col and y is row) and isinstance(solving_puzzle[y][x], list):
                                    for digit in solving_puzzle[y][x]:
                                        if digit in cell_possibles:
                                            cell_possibles.remove(digit)
                        if len(cell_possibles) == 1:
                            # we have a hidden single
                            progress = True
                            solved_one = True
                            solving_puzzle[row][col] = cell_possibles[0]
    return solved_one


def get_upper_left(row, col):
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
    return xi, yi


def is_solved(puzzle):
    for row in range(9):
        for col in range(9):
            if isinstance(puzzle[row][col], list):
                return False
    return True
