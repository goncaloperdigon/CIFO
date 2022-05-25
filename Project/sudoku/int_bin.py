from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from copy import deepcopy


def get_fitness(self):
    """A fitness function that returns the
    number of 1's occurring in the binary representation of a number

    Returns:
        int: the number of 1's in the binary representation.
    """
    return self.representation.count(1)


def get_neighbours(self):
    """A neighbourhood function for the int_bin problem. Flips the bits

    Returns:
        list: a list of individuals
    """
    n = [deepcopy(self.representation) for i in range(len(self.representation))]

    for count, i in enumerate(n):
        if i[count] == 1:
            i[count] = 0
        elif i[count] == 0:
            i[count] = 1

    n = [Individual(i) for i in n]
    return n


# Monkey patching
Individual.get_fitness = get_fitness
Individual.get_neighbours = get_neighbours

pop = Population(size=1, optim="max", sol_size=4,
                 valid_set=[0, 1], replacement=True)

hill_climb(pop, log=0)
sim_annealing(pop)
