from random import randint, sample
import numpy as np

with open('sudoku_data.txt') as f:
    initial_data = np.loadtxt(f).reshape((9, 9)).astype(int)

def binary_mutation(individual):
    """Binary mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Raises:
        Exception: When individual is not binary encoded.py

    Returns:
        Individual: Mutated Individual
    """
    mut_point = randint(0, len(individual) - 1)

    if individual[mut_point] == 0:
        individual[mut_point] = 1
    elif individual[mut_point] == 1:
        individual[mut_point] = 0
    else:
        raise Exception(
            f"Trying to do binary mutation on {individual}. But it's not binary.")

    return individual


def swap_mutation(individual):
    """Swap mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    # Position of the start and end of substring
    # select a random row of the sudoku matrix
    mut_row = sample(range(len(individual)), 1)
    # select 2 random points from that row
    mut_points = sample(range(len(individual[mut_row[0]])), 2)

    # store the indexes of the initial sudoku set where the value is not 0 (unchangeable values)
    index_list = [i for i, e in enumerate(initial_data[mut_row[0]]) if e != 0]

    # Invert for the mutation
    # if one of the mutation points is an unchangeable  value, sample again
    while ((mut_points[0] in index_list) or (mut_points[1] in index_list)):
        mut_points = sample(range(len(individual[mut_row[0]])), 2)

    # This method assumes that the second point is after (on the right of) the first one
    # Sort the list
    mut_points.sort()
    #Swap
    individual[mut_row[0]][mut_points[0]], individual[mut_row[0]][mut_points[1]] = individual[mut_row[0]][mut_points[1]], individual[mut_row[0]][mut_points[0]]

    return individual


def inversion_mutation(individual):
    """Inversion mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """

    #initial_set = np.array(initial_data).flatten(order='C').tolist()
    #individual = np.array(individual).flatten(order='C').tolist()


    # Position of the start and end of substring
    #select a random row of the sudoku matrix
    mut_row = sample(range(len(individual)), 1)
    #select 2 random points from that row
    mut_points = sample(range(len(individual[mut_row[0]])), 2)

    # store the indexes of the initial sudoku set where the value is not 0 (unchangeable values)
    index_list = [i for i, e in enumerate(initial_data[mut_row[0]]) if e != 0]

    # Invert for the mutation
    #if one of the mutation points is an unchangeable  value, sample again
    while ((mut_points[0] in index_list) or (mut_points[1] in index_list)):
        mut_points = sample(range(len(individual[mut_row[0]])), 2)

    # This method assumes that the second point is after (on the right of) the first one
    # Sort the list
    mut_points.sort()

    individual[mut_row[0]][mut_points[0]:mut_points[1]] = individual[mut_row[0]][mut_points[0]:mut_points[1]][::-1]

    return individual


if __name__ == '__main__':
    test = [6, 1, 3, 5, 2, 4, 7]
    test = inversion_mutation(test)

