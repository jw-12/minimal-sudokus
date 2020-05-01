"""
    Script to generate a large quantity of sudoku solutions to an output file.
"""

from generate_solution import generate_solution


def batch_create_solutions(n, fname):

    for i in range(1, n+1):
        if i % 1000 == 0:
            print("{} created".format(i))
        soln = generate_solution()
        soln = [str(y) for x in soln for y in x]

        f = open(fname, "a")
        f.write("{},".format(i))
        for el in soln:
            f.write(el)
        f.write("\n")
        f.close()


if __name__ == '__main__':
    batch_create_solutions(1, "output2.csv")
