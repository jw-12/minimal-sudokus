""" tests for the second version """

from backwards_from_solution import *


def test_new_config():

    global validator_count

    sol_str = "864371259325849761971265843436192587198657432257483916689734125713528694542916378"
    puz_str = "004300209005009001070060043006002087190007400050083000600000105003508690042910300"
    i_ind = 0
    j_ind = 0
    sol_list = [[] for i in range(9)]
    puz_list = [[] for i in range(9)]

    # get indexes to remove
    # convert sol_str into lists
    for str_index, el in enumerate(puz_str):
        if j_ind > 8:
            i_ind += 1
            j_ind = 0
        sol_list[i_ind].append(int(sol_str[str_index]))
        puz_list[i_ind].append(int(puz_str[str_index]))
        j_ind += 1

    print("SOLUTION:")
    for r in sol_list:
        print(r)
    print("\nPUZZLE:")
    for r in puz_list:
        print(r)
    ret1 = validator(puz_list, False)
    ret2 = validator(puz_list, True)

    print("Solution 1:")
    for r in ret1:
        print(r)
    print("Solution 2:")
    for r in ret2:
        print(r)
    print("Matched: {}".format(compare_solutions(ret1, ret2)))


def test_new_config_multipleSoln():
    grid = [
        [9, 1, 7, 3, 4, 6, 8, 2, 5],
        [2, 4, 8, 7, 1, 5, 6, 3, 9],
        [5, 3, 6, 8, 9, 2, 1, 4, 7],
        [8, 7, 2, 9, 3, 4, 5, 6, 1],
        [6, 9, 1, 2, 5, 7, 4, 8, 3],
        [4, 5, 3, 6, 8, 1, 9, 7, 2],
        [1, 2, 5, 4, 7, 8, 3, 9, 6],
        [7, 8, 9, 5, 6, 3, 2, 1, 4],
        [3, 6, 4, 1, 2, 9, 7, 5, 8]
    ]

    print("Solution:")
    for r in grid:
        print(r)

    grid[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    grid[1] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    grid[2] = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    print("Puzzle:")
    for r in grid:
        print(r)

    ret1 = validator(grid, False)
    ret2 = validator(grid, True)
    print("Solution 1:")
    for r in ret1:
        print(r)
    print("Solution 2:")
    for r in ret2:
        print(r)
    print("Match: {}".format(compare_solutions(ret1, ret2)))


def test_17_clue():
    global validator_count

    puz_str = "000801000000000043500000000000070800000000100020030000600000075003400000000200600"  # 17 clue puzzle
    sol_str = "237841569186795243594326718315674892469582137728139456642918375853467921971253684"  # soln to above
    puz_list = [[] for i in range(9)]

    i_ind = 0
    j_ind = 0

    for str_index, el in enumerate(puz_str):
        if j_ind > 8:
            i_ind += 1
            j_ind = 0
        puz_list[i_ind].append(int(puz_str[str_index]))
        j_ind += 1

    print("Puzzle:")
    for r in puz_list:
        print(r)

    int_len_list = list()
    for i in range(9):
        for j in range(9):
            int_len_list.append(len(get_intersection(i, j, puz_list)))

    """for el in int_len_list:
        print(el)"""

    ret1 = validator(puz_list, False)
    print("Finished Ascending")
    validator_count = 0
    ret2 = validator(puz_list, True)
    print("Finished Descending")
    print("Match: {}".format(compare_solutions(ret1, ret2)))

    print("Solution 1:")
    for r in ret1:
        print(r)
    print("Solution 2:")
    for r in ret2:
        print(r)