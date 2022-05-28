from random import randint
def row_crossover (p1 , p2):
    """Implementation of specific sudoku crossover, where several rows
    are switched entirely and at random

    Args:
        Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover."""

    crossover_points = randint(2, 7)
    row_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    offspring1 = p1
    offspring2 = p2

    for i in range (crossover_points):
        co_point = row_indexes.pop(randint(0, row_indexes.length()))
        offspring1[co_point] = p2[co_point]
        offspring2[co_point] = p1[co_point]

    return offspring1,  offspring2
