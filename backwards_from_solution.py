"""
    build a minimal sudoku backwards from a known solution
"""
import os
import random
import datetime as dt
import psycopg2 as pg
from dotenv import load_dotenv
import logging

from generate_solution import generate_solution, get_subgrid_number

validator_count = 0


""" Keep trying to remove cells and verifying solution to grid is still unique. 
Writes relevant data to postgres database """


def backwards_from_solution(conn, cur):

    global validator_count  # used to count branches

    start_exec = dt.datetime.now()

    solution = generate_solution()
    stable_copy = [r.copy() for r in solution]
    removed_indexes = list()

    # write solution to output file in case of stall
    f = open("current_grid.txt", "w")
    for r in solution:
        for el in r:
            f.write("{}".format(el))
    f.close()

    try:
        while len(removed_indexes) < 81:
            rem_copy = [r.copy() for r in stable_copy]  # copy to the removal copy which we can try remove cells from
            while True:
                # Randomly select an index to remove from the grid
                # keep randomly picking if have already tried this index
                rand_i = random.randint(0, 8)
                rand_j = random.randint(0, 8)
                if [rand_i, rand_j] not in removed_indexes:
                    removed_indexes.append([rand_i, rand_j])  # add to the list of removed indexes
                    break

            # remove this index from the grid
            rem_copy[rand_i][rand_j] = 0

            validator_count = 0
            ret1 = validator(rem_copy, False)
            tmp_branch_asc = validator_count

            validator_count = 0
            ret2 = validator(rem_copy, True)
            tmp_branch_desc = validator_count

            if compare_solutions(ret1, ret2):
                # safe to remove this index and continue
                stable_copy[rand_i][rand_j] = 0
                branch_asc = tmp_branch_asc
                branch_desc = tmp_branch_desc

            # otherwise changes will be reset at beginning of next iteration

        sol_str = ""
        puz_str = ""
        num_erasures = 0
        for i in range(9):
            for j in range(9):
                sol_str += str(solution[i][j])
                puz_str += str(stable_copy[i][j])
                if stable_copy[i][j] == 0:
                    num_erasures += 1

        end_exec = dt.datetime.now()

        cur.execute("INSERT INTO minimal_sudokus (puzzle, solution, start_exec, end_exec, num_erasures, ascending_branches, descending_branches) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (puz_str, sol_str, start_exec, end_exec, num_erasures, branch_asc, branch_desc))
        conn.commit()

    except Exception:
        logging.error("Error Info: ", exc_info=True)
        print("Current Grid: ")
        for r in solution:
            print(r)
        print("----")

    return


def get_intersection(i, j, grid):   # return a list containing the candidates which can be used in a given cell
    used_in_row = [el for el in grid[i] if el != 0]
    used_in_col = list()
    used_in_subgrid = list()
    subgrid_number = get_subgrid_number(i, j)

    for ind in range(9):
        used_in_col.append(grid[ind][j])
        for jnd in range(9):
            if get_subgrid_number(ind, jnd) == subgrid_number:
                used_in_subgrid.append(grid[ind][jnd])

    return [x for x in range(1, 10) if x not in used_in_row and x not in used_in_col and x not in used_in_subgrid]


def validator(grid, permuteDescending):   # ensure valid grid - validates recursively

    val_copy = [list.copy(r) for r in grid]   # copy on each instance to avoid overlapping changes

    global validator_count
    validator_count += 1

    for i in range(9):
        for j in range(9):
            if val_copy[i][j] == 0:
                # get overlap of the three constraints - only potential valid digits
                intersection = get_intersection(i, j, val_copy)

                if len(intersection) > 0:

                    if len(intersection) > 1:
                        # we need to branch on this cell as there are still more options for this cell remaining

                        # ascending/descending order of values filled into the cells
                        intersection.sort(reverse=permuteDescending)

                        for el in intersection:
                            sub_valcopy = [r.copy() for r in val_copy]
                            sub_valcopy[i][j] = el
                            ret = validator(sub_valcopy, permuteDescending)
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


def compare_solutions(sol1, sol2):   # return True if solutions are the same
    for ind, el in enumerate(sol1):
        if sol2[ind] != el:
            return False
    return True


def main():

    local = False  # true if DB instance running locally

    load_dotenv()  # read in the environment variables
    if local:
        host = os.environ['DB_LOCAL_HOST']
    else:
        host = os.environ['DB_REMOTE_HOST']
    conn = pg.connect(user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'], host=host, port=os.environ['DB_PORT'],
                      database=os.environ['DB_DATABASE'])
    cur = conn.cursor()

    for i in range(1000):
        backwards_from_solution(conn, cur)

    # close connection
    if conn:
        cur.close()
        conn.close()
        print("Closing Connection to Database")


if __name__ == '__main__':
    main()
