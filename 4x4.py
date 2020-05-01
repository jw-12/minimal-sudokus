""" File used to generate and inspect all 4 by 4 sudoku grids """
import itertools

grids = list()
four_clue_count = 0


def get_subgrid_4x4(i, j):
    if i < 2:
        if j < 2:
            return 0
        else:
            return 1
    else:
        if j < 2:
            return 2
        else:
            return 3


def index_to_ij_4x4(index):
    """
    Convert single digit index to row, col for 4x4 case
    :param index: single digit to convert
    :return: list of the form [row, col]
    """
    if index < 4:
        i = 0
    elif index < 8:
        i = 1
    elif index < 12:
        i = 2
    else:
        i = 3

    return [i, index % 4]


def get_intersection_4x4(i, j, grid):   # return a list containing the candidates which can be used in a given cell
    used_in_row = [el for el in grid[i] if el != 0]
    used_in_col = list()
    used_in_subgrid = list()
    subgrid_number = get_subgrid_4x4(i, j)

    for ind in range(4):
        used_in_col.append(grid[ind][j])
        for jnd in range(4):
            if get_subgrid_4x4(ind, jnd) == subgrid_number:
                used_in_subgrid.append(grid[ind][jnd])

    return [x for x in range(1, 5) if x not in used_in_row and x not in used_in_col and x not in used_in_subgrid]


def validator_4x4(grid, permuteDescending):   # ensure valid grid - validates recursively

    val_copy = [list.copy(r) for r in grid]   # copy on each instance to avoid overlapping changes

    #global validator_count
    #validator_count += 1

    for i in range(4):
        for j in range(4):
            if val_copy[i][j] == 0:
                # get overlap of the three constraints - only potential valid digits
                intersection = get_intersection_4x4(i, j, val_copy)

                if len(intersection) > 0:

                    if len(intersection) > 1:
                        # we need to branch on this cell as there are still more options for this cell remaining

                        # ascending/descending order of values filled into the cells
                        intersection.sort(reverse=permuteDescending)

                        for el in intersection:
                            sub_valcopy = [r.copy() for r in val_copy]
                            sub_valcopy[i][j] = el
                            ret = validator_4x4(sub_valcopy, permuteDescending)
                            if ret:
                                return ret
                        return  # if none of these attempted intersection values are valid
                    else:
                        # there is only 1 element remaining for this cell - insert and continue iterating through cells
                        insert_value = intersection.pop()

                        val_copy[i][j] = insert_value   # then add next number in here and move onto next index

                else:
                    return   # since this is not a valid route (empty intersection on an empty cell)
    return val_copy


def generator_4x4(grid):   # ensure valid grid - validates recursively

    val_copy = [list.copy(r) for r in grid]   # copy on each instance to avoid overlapping changes

    global grid_count

    for i in range(4):
        for j in range(4):
            if val_copy[i][j] == 0:
                # get overlap of the three constraints - only potential valid digits
                intersection = get_intersection_4x4(i, j, val_copy)

                if i == j == 3:
                    #print()
                    if len(intersection) == 0:
                        """for r in val_copy:
                            print(r)"""
                        grids.append(val_copy)

                    else:
                        for el in intersection:
                            val_copy[i][j] = el
                            """for r in val_copy:
                                print(r)"""
                            grids.append(val_copy)

                if len(intersection) > 0:

                    if len(intersection) > 1:
                        # we need to branch on this cell as there are still more options for this cell remaining

                        # ascending/descending order of values filled into the cells
                        intersection.sort()

                        for el in intersection:
                            sub_valcopy = [r.copy() for r in val_copy]
                            sub_valcopy[i][j] = el

                            ret = generator_4x4(sub_valcopy)
                            #if ret:
                            #    return ret
                        return  # if none of these attempted intersection values are valid
                    else:
                        # there is only 1 element remaining for this cell - insert and continue iterating through cells
                        insert_value = intersection.pop()

                        val_copy[i][j] = insert_value   # then add next number in here and move onto next index

                else:
                    return   # since this is not a valid route (empty intersection on an empty cell)
    return val_copy


def generate_all_4by4():
    """
    Steps in generating all 4 by 4:
        1. Generate permutations of top left subgrid
        FOREACH perm:
            2. Fill top left subgrid
            3. Call generator
    """

    perm = itertools.permutations([1, 2, 3, 4])

    for el in perm:
        grid = [
            [el[0], el[1], 0, 0],
            [el[2], el[3], 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]

        generator_4x4(grid)


def minimum_clues_4x4(grid, num_clues):
    """
    Obtain minimum number of clues possible for a given 4x4 grid
    :param grid: completed 4x4 sudoku solution to be 'poked'
    """
    global four_clue_count

    comb = itertools.combinations(range(16), 16 - num_clues)  # trying for num_clues = 4 case
    ij_comb = [[index_to_ij_4x4(index) for index in c] for c in comb]

    for row in ij_comb:
        grid_copy = [r.copy() for r in grid]

        for el in row:
            grid_copy[el[0]][el[1]] = 0

        ret1 = validator_4x4(grid_copy, False)
        ret2 = validator_4x4(grid_copy, True)

        is_same = same_grids(ret1, ret2)

        if is_same:
            """print("VALID")
            for r in grid_copy:
                print(r)"""
            four_clue_count += 1
            return  # will no longer search for minimal sudokus on this grid. Therefore the count will only ever count 1 per grid


def same_grids(grid1, grid2):
    for ind, row in enumerate(grid1):
        if row != grid2[ind]:
            return False
    return True


if __name__ == '__main__':
    generate_all_4by4()
    for g in grids:
        minimum_clues_4x4(g, 4)
    print(four_clue_count)
