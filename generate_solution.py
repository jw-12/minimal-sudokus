"""
    Randomly generate a sudoku codeword and return as a list
"""

import random


def generate_solution():

    while True:
        grid = [[None] * 9 for i in range(9)]

        """ 
            These contain the remaining possible numbers for each row, column, subgrid
        """
        rows = [set(range(1, 10)) for i in range(9)]
        cols = [set(range(1, 10)) for i in range(9)]
        subgrids = [set(range(1, 10)) for i in range(9)]

        try:
            """
                Loop through all cells, if invalid don't go back - just discard and start again
            """
            for i in range(9):
                for j in range(9):

                    if i <= 2:  # i.e. i in [0, 1, 2]
                        if j <= 2:
                            sub_num = 0
                        elif 2 < j < 6:
                            sub_num = 1
                        else:
                            sub_num = 2
                    elif 2 < i < 6:
                        if j <= 2:
                            sub_num = 3
                        elif 2 < j < 6:
                            sub_num = 4
                        else:
                            sub_num = 5
                    else:
                        if j <= 2:
                            sub_num = 6
                        elif 2 < j < 6:
                            sub_num = 7
                        else:
                            sub_num = 8

                    valid_options = list(rows[i].intersection(cols[j]).intersection(subgrids[sub_num]))
                    insert_val = random.choice(valid_options)
                    rows[i].remove(insert_val)
                    cols[j].remove(insert_val)
                    subgrids[sub_num].remove(insert_val)
                    grid[i][j] = insert_val

            return grid

        except IndexError as e:
            pass
