"""
    build a minimal sudoku backwards from a known solution
"""
import random
import sys

from generate_solution import generate_solution, get_subgrid_number

validator_count = 0
output_solutions = list()


def backwards_from_solution():
    solution = generate_solution()
    copy = [list.copy(r) for r in solution]

    rows = [[] for i in range(9)]
    cols = [[] for i in range(9)]
    subgrids = [[] for i in range(9)]

    f = open("sudoku_solution.txt", "w")
    for r in solution:
        print(r)
        f.write(",".join([str(e) for e in r]))
        f.write("\n")
    f.close()

    # Randomly select an index to remove from the grid
    rand_i = random.randint(0, 8)
    rand_j = random.randint(0, 8)

    for r in copy:
        print(r)

    print("\n")

    remove_cell(rand_i, rand_j, rows, cols, subgrids, solution, copy)

    for r in copy:
        print(r)

    # now validate the grid
    validator(copy, rows, cols, subgrids)

    return


def remove_cell(i, j, rows, cols, subgrids, solution, copy):
    #print("Removing Index {},{}".format(i,j))
    copy[i][j] = None
    rows[i].append(solution[i][j])
    cols[j].append(solution[i][j])
    subgrids[get_subgrid_number(i, j)].append(solution[i][j])
    return


def validator(grid, rows, cols, subgrids, permuteDescending):   # ensure valid grid
    # loop through i, j and use subgrid as constraint on this
    val_copy = [list.copy(r) for r in grid]  # todo: remove this copying since the passed down grid is a copy

    global validator_count, output_solutions
    validator_count += 1

    for i in range(9):
        for j in range(9):
            if val_copy[i][j] is None:
                # get overlap of the three constraints - only potential valid digits
                intersection = [x for x in rows[i] if x in cols[j] and x in subgrids[get_subgrid_number(i, j)]]

                if len(intersection) > 0:

                    if len(intersection) > 1:
                        # we need to branch on this cell as there are still more options for this cell remaining

                        # ascending/descending order of values filled into the cells
                        intersection.sort(reverse=permuteDescending)

                        for el in intersection:
                            sub_valcopy = [r.copy() for r in val_copy]
                            sub_valcopy[i][j] = el
                            row_copy = [r.copy() for r in rows]
                            cols_copy = [r.copy() for r in cols]
                            subgrids_copy = [r.copy() for r in subgrids]
                            row_copy[i].remove(el)
                            cols_copy[j].remove(el)
                            subgrids_copy[get_subgrid_number(i, j)].remove(el)
                            ret = validator(sub_valcopy, row_copy, cols_copy, subgrids_copy, permuteDescending)
                            if ret:
                                return ret
                        return  # if none of these attempted intersection values are valid
                    else:
                        # there is only 1 element remaining for this cell - insert and continue iterating through cells
                        insert_value = intersection.pop()
                        rows[i].remove(insert_value)
                        cols[j].remove(insert_value)
                        subgrids[get_subgrid_number(i, j)].remove(insert_value)

                        val_copy[i][j] = insert_value   # then add next number in here and recurse

                        # if there are no elements in the constraint lists
                        if not (any(rows) and any(cols) and any(subgrids)):
                            print("Solution Found:")
                            for r in val_copy:
                                print(r)
                            return val_copy
                else:
                    return   # since this is not a valid route (empty intersection with None in a cell)


def test_validator_againstDuplicateGrid():
    grid = [
        [9,1,7,3,4,6,8,2,5],
        [2,4,8,7,1,5,6,3,9],
        [5,3,6,8,9,2,1,4,7],
        [8,7,2,9,3,4,5,6,1],
        [6,9,1,2,5,7,4,8,3],
        [4,5,3,6,8,1,9,7,2],
        [1,2,5,4,7,8,3,9,6],
        [7,8,9,5,6,3,2,1,4],
        [3,6,4,1,2,9,7,5,8]
]

    print("Original Solution:")
    for r in grid:
        print(r)
    print("\n")

    output_solutions.append(grid)

    rows1 = [[] for i in range(9)]
    cols1 = [[] for i in range(9)]
    subgrids1 = [[] for i in range(9)]

    copy1 = [list.copy(r) for r in grid]

    for j in range(9):
        remove_cell(0, j, rows1, cols1, subgrids1, grid, copy1)
    for j in range(9):
        remove_cell(1, j, rows1, cols1, subgrids1, grid, copy1)
    for j in range(9):
        remove_cell(2, j, rows1, cols1, subgrids1, grid, copy1)
    for j in range(9):
        remove_cell(3, j, rows1, cols1, subgrids1, grid, copy1)

    # copy grid config
    [copy2, rows2, cols2, subgrids2] = safe_grid_copy(copy1, rows1, cols1, subgrids1)

    print("Grid to Solve:")
    for r in copy1:
        print(r)

    ret1 = validator(copy1, rows1, cols1, subgrids1, False)
    print("Val Count Ascending: {}\n".format(validator_count))

    ret2 = validator(copy2, rows2, cols2, subgrids2, True)
    print("Val Count Descending: {}".format(validator_count))

    matched_solutions = True
    for ind, el in enumerate(ret1):
        if ret2[ind] != el:
            matched_solutions = False

    print("Solutions Match? {}".format(matched_solutions))

    return


def test_using_kaggleSource():

    global validator_count

    sol_str = "864371259325849761971265843436192587198657432257483916689734125713528694542916378"
    puz_str = "004300209005009001070060043006002087190007400050083000600000105003508690042910300"
    i_ind = 0
    j_ind = 0
    indexes_to_remove = list()
    sol_list = [[] for i in range(9)]

    # get indexes to remove
    # convert sol_str into lists
    for str_index, el in enumerate(puz_str):
        if j_ind > 8:
            i_ind += 1
            j_ind = 0
        sol_list[i_ind].append(int(sol_str[str_index]))
        if el == "0":
            indexes_to_remove.append([i_ind, j_ind])
        j_ind += 1

    output_solutions.append(sol_list)

    rows1 = [[] for i in range(9)]
    cols1 = [[] for i in range(9)]
    subgrids1 = [[] for i in range(9)]
    sol_copy1 = [x.copy() for x in sol_list]

    print("Original Grid:")
    for r in sol_list:
        print(r)
    print("\n")

    for el in indexes_to_remove:
        remove_cell(el[0], el[1], rows1, cols1, subgrids1, sol_list, sol_copy1)

    # copy the grid configuration to be used in second validator
    [sol_copy2, rows2, cols2, subgrids2] = safe_grid_copy(sol_copy1, rows1, cols1, subgrids1)

    print("Grid to Solve:")
    for r in sol_copy1:
        print(r)
    print("\n")

    ret1 = validator(sol_copy1, rows1, cols1, subgrids1, False)  # ascending first
    print("Val Count Ascending: {}\n".format(validator_count))

    validator_count = 0

    ret2 = validator(sol_copy2, rows2, cols2, subgrids2, True)  # now descending
    print("Val Count Descending: {}".format(validator_count))

    matched_solutions = True
    for ind, el in enumerate(ret1):
        if ret2[ind] != el:
            matched_solutions = False

    print("Solutions Match? {}".format(matched_solutions))


def safe_grid_copy(grid, rows, cols, subgrids):  # returns list of the grid config in the form [grid, rows, cols, subgrids]
    return [[r.copy() for r in grid], [r.copy() for r in rows], [r.copy() for r in cols], [r.copy() for r in subgrids]]


def main():
    #backwards_from_solution()
    test_validator_againstDuplicateGrid()
    #test_using_kaggleSource()


if __name__ == '__main__':
    main()