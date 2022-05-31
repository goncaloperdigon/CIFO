from random import uniform, choice, sample
from operator import attrgetter
import numpy as np


def fps(population): # only works for maximization
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """

    if population.optim == "max":
        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual

    elif population.optim == "min":
        raise NotImplementedError

    else:
        raise Exception("No optimization specified (min or max).")


def tournament(population, size=100):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: Best individual in the tournament.
    """

    # Select individuals based on tournament size
    tournament = [choice(population.individuals) for i in range(size)]
    # Check if the problem is max or min
    if population.optim == 'max':
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == 'min':
        return min(tournament, key=attrgetter("fitness"))
    else:
        raise Exception("No optimization specified (min or max).")


def ranking(population):

    #randomly choose (with repetition) individuals from the population
    ranking = [choice(population.individuals) for i in range(population.size)]

    top_half_size = int(population.size/2)

    if population.optim == 'max':
        #sort individuals by fitness
        fitness_ranking = sorted(ranking, key=attrgetter("fitness"), reverse=True)
        #select only the top half
        selected = np.array(sample(fitness_ranking[:top_half_size], 1)).reshape((9, 9)).astype(int).tolist()
        return selected

    elif population.optim == 'min':
        #sort individuals by fitness
        fitness_ranking = sorted(ranking, key=attrgetter("fitness"), reverse=False)
        #select only the top half
        selected = np.array(sample(fitness_ranking[:top_half_size], 1)).reshape((9, 9)).astype(int).tolist()
        return selected
    else:
        raise Exception("No optimization specified (min or max).")
