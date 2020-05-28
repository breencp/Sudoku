# file: techniques.py
# author: Christopher Breen
# date: May 24, 2020

# from .xwing import x_wing


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

        # testing x-wing
#        if x_wing(puzzle_to_solve):
#            techniques_utilized.add("X-Wing")
#            progress = True

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
                            cell_possibles = [i for i in cell_possibles if i not in solving_puzzle[row][x]]
                    if len(cell_possibles) == 1:
                        # we have a hidden single
                        progress = True
                        solved_one = True
                        solving_puzzle[row][col] = cell_possibles[0]

                    if isinstance(solving_puzzle[row][col], list):
                        cell_possibles = solving_puzzle[row][col][:]
                        for y in range(9):
                            if y is not row and isinstance(solving_puzzle[y][col], list):
                                cell_possibles = [i for i in cell_possibles if i not in solving_puzzle[y][col]]
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
                                    cell_possibles = [i for i in cell_possibles if i not in solving_puzzle[y][x]]
                        if len(cell_possibles) == 1:
                            # we have a hidden single
                            progress = True
                            solved_one = True
                            solving_puzzle[row][col] = cell_possibles[0]
    return solved_one

def x_wing(solving_puzzle):
    progress = True
    solved_one = False
    while progress:
        progress = False
        for row in range(9):
            for col in range(9):
                if isinstance(solving_puzzle[row][col], list):
                    cell_possibles = solving_puzzle[row][col][:]
                    for x in range(9):
                        if x is not col and isinstance(solving_puzzle[row][x], list):
                            for digit in solving_puzzle[row][x][:]:
                                if digit in cell_possibles:
                                    for y in range(9):
                                        if y is not col and y is not x and isinstance(solving_puzzle[row][y], list):
                                            if digit not in solving_puzzle[row][y][:]:
                                                # Possible X-Wing In Rows
                                                for z in range(9):
                                                    if z is not row and isinstance(solving_puzzle[z][col]):
                                                        if digit in solving_puzzle[z][col][:] and digit in solving_puzzle[z][x][:] and digit not in solving_puzzle[z][y][:]:
                                                            # We have an X_Wing In Rows
                                                            progress = True
                                                            solved_one = True
                                                            #Remove Digit from cell possibility of colunms col and x, Except for [row][col] and [row][x], [z, col] and [z,x]
                                                            for i in range(9):
                                                                if i is not row and i is not z and (isinstance(solving_puzzle([i][col], list) | isinstance(solvable_puzzle([i][x], list)))):
                                                                    if digit in solving_puzzle[i][col][:]:
                                                                        solving_puzzle[i][col][:].remove(digit)
                                                                    if digit in solving_puzzle[i][x][:]:
                                                                        solving_puzzle[i][x][:].remove(digit)

                        if x is not row and isinstance(solving_puzzle[x][col], list):
                            for digit in cell_possibles:
                                if digit in cell_possibles:
                                    for y in range(9):
                                        if y is not row and y is not x and isinstance(solving_puzzle[y][col], list):
                                            if digit not in solving_puzzle[y][col][:]:
                                                # Possible X-Wing In Columns
                                                for z in range(9):
                                                    if z is not col and isinstance(solving_puzzle[row][z]):
                                                        if digit in solving_puzzle[row][z][:] and digit in solving_puzzle[x][z][:] and digit not in solving_puzzle[y][z][:]:
                                                            # We have an X_Wing In Colums
                                                            progress = True
                                                            solved_one = True
                                                            # Remove Digit from cell possibility of rows row and x, Except for [row][col] and [x][col]
                                                            for i in range(9):
                                                                if i is not col and i is not z and (isinstance(solving_puzzle[row][i], list) | isinstance(solving_puzzle[x][i], list)):
                                                                    if digit in solving_puzzle[row][i][:]:
                                                                        solving_puzzle[row][i][:].remove(digit)
                                                                    if digit in solving_puzzle[x][i][:]:
                                                                        solving_puzzle[x][i][:].remove(digit)

    return solved_one

def xy_wing(solving_puzzle):
    progress = True
    solved_one = False
    while progress:
        progress = False
        for row in range(9):
            for col in range(9):
                # Assumes solving_puzzle[row][col] is the middle and looks for the wings
                if isinstance(solving_puzzle[row][col], list):
                    cell_possibles = solving_puzzle[row][col][:]
                    if len(cell_possibles) == 2:
                        first_possibility = cell_possibles[0]
                        second_possibility = cell_possibles[1]
                        # Scan Row for another cell with one of those pencil marks
                        for x in range(9):
                            if x is not col and isinstance(solving_puzzle[row][x], list):
                                if len(solving_puzzle[row][x][:]) == 2:
                                    row_first_element = solving_puzzle[row][x][0]
                                    row_second_element = solving_puzzle[row][x][1]
                                    if (row_first_element == first_possibility ^ row_first_element == second_possibility) \
                                            and (row_second_element not in [first_possibility, second_possibility]):
                                        if row_first_element == first_possibility:
                                            # common_element = row_first_element
                                            wing_common = row_second_element
                                            # Scan col for wings
                                            for y in range(9):
                                                if y is not row and isinstance(solving_puzzle[y][col], list) and len(solving_puzzle[y][col][:]) == 2:
                                                    if solving_puzzle[y][col][:] == [second_possibility, wing_common] | \
                                                            solving_puzzle[y][col][:] == [wing_common, second_possibility]:
                                                        # XY-Wing (Middle-[row,col] Wings-([row,x] and [y,col]))
                                                        progress = True
                                                        solved_one = True
                                                        # Look for intersectng cells of the Wings and safely remove wing_common from the intersecting cell
                                                        if wing_common in solving_puzzle[y][x][:]:
                                                            solving_puzzle[y][x][:].remove(wing_common)

                                            # Scan block for wings
                                            xi, yi = get_upper_left(row, col)
                                            for i in range(yi, yi + 3):
                                                for j in range(xi, xi + 3):
                                                    if not (j is col and i is row) and isinstance(solving_puzzle[i][j], list) \
                                                            and len(solving_puzzle[i][j][:] == 2):
                                                        if solving_puzzle[i][j][:] == [second_possibility, wing_common] | \
                                                                solving_puzzle[i][j][:] == [wing_common, second_possibility]:
                                                            # XY-Wing (Middle-[row,col] Wings-([row,x] and [i,j]))
                                                            progress = True
                                                            solved_one = True
                                                            # Look for intersectng cells of the Wings and safely remove wing_common from the intersecting cell
                                                            wing_xi, wing_yi = get_upper_left(row, x)
                                                            for m in range(wing_yi, wing_yi + 3):
                                                                for n in range(wing_xi, wing_xi + 3):
                                                                    if wing_common in solving_puzzle[i][n][:]:
                                                                        solving_puzzle[i][n][:].remove(wing_common)

                                        elif row_first_element == second_possibility:
                                            # common_element = row_first_element
                                            wing_common = row_second_element
                                            # Scan col for wings
                                            for y in range(9):
                                                if y is not row and isinstance(solving_puzzle[y][col], list) and len(solving_puzzle[y][col][:]) == 2:
                                                    if solving_puzzle[y][col][:] == [first_possibility, wing_common] | \
                                                            solving_puzzle[y][col][:] == [wing_common, first_possibility]:
                                                        # XY-Wing (Middle-[row,col] Wings-([row,x] and [y,col]))
                                                        progress = True
                                                        solved_one = True
                                                        # Look for intersectng cells of the Wings and safely remove wing_common from the intersecting cell
                                                        if wing_common in solving_puzzle[y][x][:]:
                                                            solving_puzzle[y][x][:].remove(wing_common)

                                            # Scan block for wings
                                            xi, yi = get_upper_left(row, col)
                                            for i in range(yi, yi + 3):
                                                for j in range(xi, xi + 3):
                                                    if not (j is col and i is row) and isinstance(solving_puzzle[i][j], list) \
                                                            and len(solving_puzzle[i][j][:] == 2):
                                                        if solving_puzzle[i][j][:] == [first_possibility, wing_common] | \
                                                                solving_puzzle[i][j][:] == [wing_common,
                                                                                         first_possibility]:
                                                            # XY-Wing (Middle-[row,col] Wings-([row,x] and [i,j]))
                                                            progress = True
                                                            solved_one = True
                                                            # Look for intersectng cells of the Wings and safely remove wing_common from the intersecting cell
                                                            wing_xi, wing_yi = get_upper_left(row, x)
                                                            for m in range(wing_yi, wing_yi + 3):
                                                                for n in range(wing_xi, wing_xi + 3):
                                                                    if wing_common in solving_puzzle[i][n][:]:
                                                                        solving_puzzle[i][n][:].remove(wing_common)

                                    elif (row_second_element == first_possibility ^ row_second_element == second_possibility) \
                                            and (row_first_element not in [first_possibility, second_possibility]):
                                        if row_second_element == first_possibility:
                                            # common_element = row_second_element
                                            wing_common = row_first_element
                                            # Scan col for wings
                                            for y in range(9):
                                                if y is not row and isinstance(solving_puzzle[y][col], list) \
                                                        and len(solving_puzzle[y][col][:]) == 2:
                                                    if solving_puzzle[y][col][:] == [second_possibility, wing_common] | \
                                                            solving_puzzle[y][col][:] == [wing_common, second_possibility]:
                                                        # XY-Wing (Middle-[row,col] Wings-([row,x] and [y,col]))
                                                        progress = True
                                                        solved_one = True
                                                        if wing_common in solving_puzzle[y][x][:]:
                                                            solving_puzzle[y][x][:].remove(wing_common)

                                            # Scan block for wings
                                            xi, yi = get_upper_left(row, col)
                                            for i in range(yi, yi + 3):
                                                for j in range(xi, xi + 3):
                                                    if not (j is col and i is row) and isinstance(solving_puzzle[i][j], list) \
                                                            and len(solving_puzzle[i][j][:] == 2):
                                                        if solving_puzzle[i][j][:] == [second_possibility, wing_common] | \
                                                                solving_puzzle[i][j][:] == [wing_common,
                                                                                         second_possibility]:
                                                            # XY-Wing (Middle-[row,col] Wings-([row,x] and [i,j]))
                                                            progress = True
                                                            solved_one = True
                                                            # Look for intersectng cells of the Wings and safely remove wing_common from the intersecting cell
                                                            wing_xi, wing_yi = get_upper_left(row, x)
                                                            for m in range(wing_yi, wing_yi + 3):
                                                                for n in range(wing_xi, wing_xi + 3):
                                                                    if wing_common in solving_puzzle[i][n][:]:
                                                                        solving_puzzle[i][n][:].remove(wing_common)

                                        elif row_second_element == second_possibility:
                                            # common_element = row_second_element
                                            wing_common = row_first_element
                                            # Scan col for wings
                                            for y in range(9):
                                                if y is not row and isinstance(solving_puzzle[y][col], list) \
                                                        and len(solving_puzzle[y][col][:]) == 2:
                                                    if solving_puzzle[y][col][:] == [first_possibility, wing_common] | \
                                                            solving_puzzle[y][col][:] == [wing_common, first_possibility]:
                                                        # XY-Wing (Middle-[row,col] Wings-([row,x] and [y,col]))
                                                        progress = True
                                                        solved_one = True
                                                        # Look for intersectng cells of the Wings and safely remove wing_common from the intersecting cell
                                                        if wing_common in solving_puzzle[y][x][:]:
                                                            solving_puzzle[y][x][:].remove(wing_common)

                                            # Scan block for wings
                                            xi, yi = get_upper_left(row, col)
                                            for i in range(yi, yi + 3):
                                                for j in range(xi, xi + 3):
                                                    if not (j is col and i is row) and isinstance(solving_puzzle[i][j], list) \
                                                            and len(solving_puzzle[i][j][:] == 2):
                                                        if solving_puzzle[i][j][:] == [first_possibility, wing_common] | \
                                                                solving_puzzle[i][j][:] == [wing_common, first_possibility]:
                                                            # XY-Wing (Middle-[row,col] Wings-([row,x] and [i,j]))
                                                            progress = True
                                                            solved_one = True
                                                            # Look for intersectng cells of the Wings and safely remove wing_common from the intersecting cell
                                                            wing_xi, wing_yi = get_upper_left(row, x)
                                                            for m in range(wing_yi, wing_yi + 3):
                                                                for n in range(wing_xi, wing_xi + 3):
                                                                    if wing_common in solving_puzzle[i][n][:]:
                                                                        solving_puzzle[i][n][:].remove(wing_common)

                        # Scan Col with for another cell with one of those pencil marks
                        for x in range(9):
                            if x is not row and isinstance(solving_puzzle[x][col], list):
                                if len(solving_puzzle[x][col][:]) == 2:
                                    col_first_element = solving_puzzle[x][col][0]
                                    col_second_element = solving_puzzle[x][col][1]
                                    if (
                                            col_first_element == first_possibility ^ col_first_element == second_possibility) \
                                            and (col_second_element not in [first_possibility, second_possibility]):
                                        if col_first_element == first_possibility:
                                            # common_element = col_first_element
                                            wing_common = col_second_element
                                            # Scan block for wings
                                            xi, yi = get_upper_left(row, col)
                                            for i in range(yi, yi + 3):
                                                for j in range(xi, xi + 3):
                                                    if not (j is col and i is row) and isinstance(solving_puzzle[i][j], list) \
                                                            and len(solving_puzzle[i][j][:] == 2):
                                                        if solving_puzzle[i][j][:] == [second_possibility, wing_common] | \
                                                                solving_puzzle[i][j][:] == [wing_common, second_possibility]:
                                                            # XY-Wing (Middle-[row,col] Wings-([x,col] and [i,j]))
                                                            progress = True
                                                            solved_one = True
                                                            # Look for intersectng cells of the Wings and safely remove wing_common from the intersecting cell
                                                            wing_xi, wing_yi = get_upper_left(x, col)
                                                            for m in range(wing_yi, wing_yi + 3):
                                                                for n in range(wing_xi, wing_xi + 3):
                                                                    if wing_common in solving_puzzle[m][j][:]:
                                                                        solving_puzzle[m][j][:].remove(wing_common)

                                        elif col_first_element == second_possibility:
                                            # common_element = col_first_element
                                            wing_common = col_second_element
                                            # Scan block for wings
                                            xi, yi = get_upper_left(row, col)
                                            for i in range(yi, yi + 3):
                                                for j in range(xi, xi + 3):
                                                    if not (j is col and i is row) and isinstance(solving_puzzle[i][j], list) \
                                                            and len(solving_puzzle[i][j][:] == 2):
                                                        if solving_puzzle[i][j][:] == [first_possibility, wing_common] | \
                                                                solving_puzzle[i][j][:] == [wing_common, first_possibility]:
                                                            # XY-Wing (Middle-[row,col] Wings-([x,col] and [i,j]))
                                                            progress = True
                                                            solved_one = True
                                                            # Look for intersectng cells of the Wings and safely remove wing_common from the intersecting cell
                                                            wing_xi, wing_yi = get_upper_left(x, col)
                                                            for m in range(wing_yi, wing_yi + 3):
                                                                for n in range(wing_xi, wing_xi + 3):
                                                                    if wing_common in solving_puzzle[m][j][:]:
                                                                        solving_puzzle[m][j][:].remove(wing_common)

                                    elif (col_second_element == first_possibility ^ col_second_element == second_possibility) \
                                            and (col_first_element not in [first_possibility, second_possibility]):
                                        if col_second_element == first_possibility:
                                            # common_element = col_second_element
                                            wing_common = col_first_element
                                            # Scan block for wings
                                            xi, yi = get_upper_left(row, col)
                                            for i in range(yi, yi + 3):
                                                for j in range(xi, xi + 3):
                                                    if not (j is col and i is row) and isinstance(solving_puzzle[i][j], list) \
                                                            and len(solving_puzzle[i][j][:] == 2):
                                                        if solving_puzzle[i][j][:] == [second_possibility, wing_common] | \
                                                                solving_puzzle[i][j][:] == [wing_common, second_possibility]:
                                                            # XY-Wing (Middle-[row,col] Wings-([x,col] and [i,j]))
                                                            progress = True
                                                            solved_one = True
                                                            # Look for intersectng cells of the Wings and safely remove wing_common from the intersecting cell
                                                            wing_xi, wing_yi = get_upper_left(x, col)
                                                            for m in range(wing_yi, wing_yi + 3):
                                                                for n in range(wing_xi, wing_xi + 3):
                                                                    if wing_common in solving_puzzle[m][j][:]:
                                                                        solving_puzzle[m][j][:].remove(wing_common)

                                        elif col_second_element == second_possibility:
                                            # common_element = col_second_element
                                            wing_common = col_first_element
                                            # Scan block for wings
                                            xi, yi = get_upper_left(row, col)
                                            for i in range(yi, yi + 3):
                                                for j in range(xi, xi + 3):
                                                    if not (j is col and i is row) and isinstance(solving_puzzle[i][j], list) \
                                                            and len(solving_puzzle[i][j][:] == 2):
                                                        if solving_puzzle[i][j][:] == [first_possibility, wing_common] | \
                                                                solving_puzzle[i][j][:] == [wing_common, first_possibility]:
                                                            # XY-Wing (Middle-[row,col] Wings-([x,col] and [i,j]))
                                                            progress = True
                                                            solved_one = True
                                                            # Look for intersectng cells of the Wings and safely remove wing_common from the intersecting cell
                                                            wing_xi, wing_yi = get_upper_left(x, col)
                                                            for m in range(wing_yi, wing_yi + 3):
                                                                for n in range(wing_xi, wing_xi + 3):
                                                                    if wing_common in solving_puzzle[m][j][:]:
                                                                        solving_puzzle[m][j][:].remove(wing_common)

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
