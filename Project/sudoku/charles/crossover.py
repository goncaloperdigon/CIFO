from random import randint, uniform, sample
import numpy as np
import random

'''

Load the initial data from the file "sudoku_data.txt"

'''

with open('charles\sudoku_data.txt') as f:
    initial_data = np.loadtxt(f).reshape((9, 9)).astype(int)

#transform initial data into a list of 81 numbers
initial_data = np.array(initial_data).flatten(order='C').tolist()

'''

Uniform crossover samples 9 crossover points and swaps the values with matching indexes between the parents

'''

def uniform_crossover(p1,p2):

    # change the representation of the parents from a 2D array to 1D array using function flatten (order = C to order by row)
    p1 = np.array(p1).flatten(order='C').tolist()
    p2 = np.array(p2).flatten(order='C').tolist()

    #sample 9 cross points
    cross_points = sample(range(1,len(p1)-2), 9)

    offspring1, offspring2 = p1,p2

    #do the swap
    for i in cross_points:
        temp = offspring1[i]
        offspring1[i] = offspring2[i]
        offspring2[i] = temp

    # return offsprings as 9x9 2D arrays
    return np.array(offspring1).reshape((9, 9)).astype(int).tolist(),  np.array(offspring2).reshape((9, 9)).astype(int).tolist()



def single_point_co(p1, p2):
    """Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """

    p1 = np.array(p1).flatten(order='C').tolist()
    p2 = np.array(p2).flatten(order='C').tolist()

    co_point = randint(1, len(p1)-2)

    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]

    return np.array(offspring1).reshape((9, 9)).astype(int).tolist(), np.array(offspring2).reshape((9, 9)).astype(int).tolist()

'''

Partially mapped crossover - code used from class

'''

def new_pmx_co(p1,p2):


    # change the representation of the parents from a 2D array to 1D array using function flatten (order = C to order by row)
    p1 = np.array(p1).flatten(order='C').tolist()
    p2 = np.array(p2).flatten(order='C').tolist()

    # store the indexes of the initial sudoku set where the value is not 0 (unchangeable values)
    index_list = [i for i, e in enumerate(initial_data) if e != 0]

    co_points = sample(range(len(p1)), 2)
    co_points.sort()

    # perform the crossover
    def PMX(x, y):
        o = [None] * len(x)

        o[co_points[0]:co_points[1]] = x[co_points[0]:co_points[1]]

        z = set(y[co_points[0]:co_points[1]]) - set(x[co_points[0]:co_points[1]])

        for i in z:
            temp = i
            index = y.index(x[y.index(temp)])
            if (o[index] is not None and index not in index_list):
                temp = index
                index = y.index(x[temp])
            o[index] = i

        while None in o:
            index = o.index(None)
            o[index] = y[index]
        return o

    o1, o2 = PMX(p1, p2), PMX(p2, p1)

    #return offsprings as 9x9 2D arrays
    return np.array(o1).reshape((9, 9)).astype(int).tolist(), np.array(o2).reshape((9, 9)).astype(int).tolist()


'''

Row crossover - several rows are switched at random

'''

def row_crossover(p1 , p2):

    num_crossover_points = randint(2, 7)
    row_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    crossover_points = sample(row_indexes, num_crossover_points)

    offspring1 = p1
    offspring2 = p2

    for i in crossover_points:
        offspring1[i] = p2[i]
        offspring2[i] = p1[i]

    return offspring1,  offspring2


if __name__ == '__main__':
    p1, p2 = [[9, 8, 4], [5, 6, 7], [1, 3, 2]], [[9, 7, 1], [2, 3, 10], [8, 5, 4]]
    #p1, p2 = [1, 2, 3, 4, 5, 6, 7, 8, 9], [9, 3, 7, 8, 2, 6, 5, 1, 4]
    #p1, p2 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], [0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3]
    #p1 = np.array(p1).flatten(order='C').tolist()
    #p2 = np.array(p2).flatten(order='C').tolist()
