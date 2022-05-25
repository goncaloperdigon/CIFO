from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from copy import deepcopy
from charles.selection import fps, tournament
from charles.mutation import swap_mutation, inversion_mutation
from charles.crossover import cycle_co, pmx_co, new_pmx_co
import numpy


def get_fitness(self):

    fitness = 0

    for row in range(0,9):
        #store the row
        row_list = self.representation[row]
        #create a dict with the number of appearances of each number in the row
        my_dict = {i:row_list.count(i) for i in row_list}
        #store only the appearances that have more than 1 appearance(duplicates)
        num_of_duplicates = dict(filter(lambda val: val[1] > 1, my_dict.items()))
        #sum all the appearances of duplicates
        sum(num_of_duplicates.values())
        #
        fitness += sum(num_of_duplicates.values())

    for column in range(0,9):
        #store the column
        column_list = self.representation[column]
        #create a dict with the number of appearances of each number in the column
        my_dict = {i:row_list.count(i) for i in column_list}
        #store only the appearances that have more than 1 appearance(duplicates)
        num_of_duplicates = dict(filter(lambda val: val[1] > 1, my_dict.items()))
        #sum all the appearances of duplicates
        sum(num_of_duplicates.values())
        fitness += sum(num_of_duplicates.values())

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            # create an empty list and store all of the values of the 3x3 block
            block_list = []
            block_list.append(self.representation[i][j])
            block_list.append(self.representation[i][j + 1])
            block_list.append(self.representation[i][j + 2])
            block_list.append(self.representation[i + 1][j])
            block_list.append(self.representation[i + 2][j])
            block_list.append(self.representation[i + 1][j + 1])
            block_list.append(self.representation[i + 1][j] + 2)
            block_list.append(self.representation[i + 2][j + 1])
            block_list.append(self.representation[i + 2][j + 2])

            # create a dict with the number of appearances of each number in the block
            my_dict = {i: block_list.count(i) for i in column_list}
            # store only the appearances that have more than 1 appearance(duplicates)
            num_of_duplicates = dict(filter(lambda val: val[1] > 1, my_dict.items()))
            # sum all the appearances of duplicates
            sum(num_of_duplicates.values())
            fitness += sum(num_of_duplicates.values())

    return int(fitness)


'''def get_neighbours(self):
    """A neighbourhood function for the TSP problem. Switches
    indexes around in pairs.

    Returns:
        list: a list of individuals
    """
    n = [deepcopy(self.representation) for i in range(len(self.representation) - 1)]

    for count, i in enumerate(n):
        i[count], i[count + 1] = i[count + 1], i[count]

    n = [Individual(i) for i in n]
    return n'''


# Monkey patching
Individual.get_fitness = get_fitness
'''Individual.get_neighbours = get_neighbours'''



pop = Population(
    size=200,
    valid_set=[1,2,3,4,5,6,7,8,9],
    optim="min",
)
#print(pop.individuals[0].representation)

pop.evolve(
    gens=1000,
    select=tournament,
    crossover=pmx_co,
    mutate=inversion_mutation,
    co_p=0.8,
    mu_p=0.2,
    elitism=True
)