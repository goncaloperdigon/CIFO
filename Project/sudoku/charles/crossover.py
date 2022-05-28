from random import randint, uniform, sample
import numpy as np
import random

with open('sudoku_data.txt') as f:
    initial_data = np.loadtxt(f).reshape((9, 9)).astype(int)

initial_data = np.array(initial_data).flatten(order='C').tolist()

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

    return offspring1, offspring2


def cycle_co(p1, p2):
    """Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    p1 = np.array(p1).flatten(order='C').tolist()
    p2 = np.array(p2).flatten(order='C').tolist()

    # Offspring placeholders - None values make it easy to debug for errors
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p2)
    # While there are still None values in offspring, get the first index of
    # None and start a "cycle" according to the cycle crossover method
    while None in offspring1:
        index = offspring1.index(None)

        val1 = p1[index]
        val2 = p2[index]

        while val1 != val2:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
            val2 = p2[index]
            index = p1.index(val2)

        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2[index]
                    offspring2[index] = p1[index]

    return np.array(offspring1).reshape((9, 9)).astype(int).tolist(), np.array(offspring2).reshape((9, 9)).astype(int).tolist()

def pmx_co(p1, p2):
    """Implementation of partially matched/mapped crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """

    #change the representation of the parents from a 2D array to 1D array using function flatten (order = C to order by row)
    p1 = np.array(p1).flatten(order='C').tolist()
    p2 = np.array(p2).flatten(order='C').tolist()

    co_points = sample(range(len(p1)), 2)
    co_points.sort()

    # dictionary creation using the segment elements from both parents
    # the dictionary will be working two ways
    keys = p1[co_points[0]:co_points[1]] + p2[co_points[0]:co_points[1]]
    values = p2[co_points[0]:co_points[1]] + p1[co_points[0]:co_points[1]]
    # segment dictionary
    segment = {keys[i]: values[i] for i in range(len(keys))}

    # empty offsprings
    o1 = [None] * len(p1)
    o2 = [None] * len(p2)

    # where pmx happens
    def pmx(o, p):
        for i, element in enumerate(p):
            # if element not in the segment, copy
            if element not in segment:
                o[i] = p[i]
            # if element in the segment, take the value of the key from
            # segment/dictionary
            else:
                o[i] = segment.get(element)
        return o

    # repeat the procedure for each offspring
    o1 = pmx(p1, p2)
    o2 = pmx(p2, p1)
    #return the offsprings as 9x9 2D list
    return np.array(o1).reshape((9, 9)).astype(int).tolist(), np.array(o2).reshape((9, 9)).astype(int).tolist()

def new_pmx_co(p1,p2):

    # change the representation of the parents from a 2D array to 1D array using function flatten (order = C to order by row)
    p1 = np.array(p1).flatten(order='C').tolist()
    p2 = np.array(p2).flatten(order='C').tolist()

    # store the indexes of the initial sudoku set where the value is not 0 (unchangeable values)
    index_list = [i for i, e in enumerate(initial_data) if e != 0]

    co_points = sample(range(len(p1)), 2)
    co_points.sort()

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

    return np.array(o1).reshape((9, 9)).astype(int).tolist(), np.array(o2).reshape((9, 9)).astype(int).tolist()
    #return o1,o2

def arithmetic_co(p1, p2):
    """Implementation of arithmetic crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    # Offspring placeholders - None values make it easy to debug for errors
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)
    # Set a value for alpha between 0 and 1
    alpha = uniform(0, 1)
    # Take weighted sum of two parents, invert alpha for second offspring
    for i in range(len(p1)):
        offspring1[i] = p1[i] * alpha + (1 - alpha) * p2[i]
        offspring2[i] = p2[i] * alpha + (1 - alpha) * p1[i]

    return offspring1, offspring2


def row_crossover(p1 , p2):
    """Implementation of specific sudoku crossover, where several rows
    are switched entirely and at random

    Args:
        Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover."""

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
    p1 = np.array(p1).flatten(order='C').tolist()
    p2 = np.array(p2).flatten(order='C').tolist()
    co_points = sample(range(len(p1)), 2)
    co_points.sort()

    o = [None] * len(p1)

    o[co_points[0]:co_points[1]] = p1[co_points[0]:co_points[1]]

    z = set(p2[co_points[0]:co_points[1]]) - set(p1[co_points[0]:co_points[1]])

    print(co_points)
    print(o)
    print(z)

      #p1 = np.array(p1).flatten(order='C').tolist()
    #p2 = np.array(p2).flatten(order='C').tolist()
