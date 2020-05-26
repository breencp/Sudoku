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
                            for digit in solving_puzzle[row][x]:
                                if digit in cell_possibles:
                                    for y in range(9):
                                        if y is not col and x != y  and isinstance(solving_puzzle[row][y], list):
                                            if digit not in solving_puzzle[row][y]:
                                                # Possible X-Wing In Rows
                                                for z in range(9):
                                                    if z is not row and isinstance(solving_puzzle[z][col]):
                                                        if digit in solving_puzzle[z][col] and digit in solving_puzzle[z][x] and digit not in solving_puzzle[z][y]:
                                                            # We have an X_Wing In Rows
                                                            progress = True
                                                            solved_one = True
                                                            #Remove Digit from cell possibility of colunms col and x, Except for [row][col] and [row][x]


                        if x is not row and isinstance(solving_puzzle[x][col], list):
                            for digit in cell_possibles:
                                if digit in cell_possibles:
                                    for y in range(9):
                                        if y is not row and x != y and isinstance(solving_puzzle[y][col], list):
                                            if digit not in solving_puzzle[y][col]:
                                                # Possible X-Wing In Columns
                                                for z in range(9):
                                                    if z is not col and isinstance(solving_puzzle[row][z]):
                                                        if digit in solving_puzzle[row][z] and digit in solving_puzzle[x][z] and digit not in solving_puzzle[y][z]:
                                                            # We have an X_Wing In Colums
                                                            progress = True
                                                            solved_one = True
                                                            # Remove Digit from cell possibility of rows row and x, Except for [row][col] and [x][col]


    return solved_one
