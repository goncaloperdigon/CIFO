from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from copy import deepcopy
from charles.selection import fps, tournament , ranking
from charles.mutation import swap_row_mutation, inversion_mutation, swap_column_mutation, random_mutation, swap_grid_mutation
from charles.crossover import cycle_co, pmx_co, new_pmx_co, row_crossover
import numpy


def get_fitness(self):

    fitness = 0

    for row in range(0,9):
        #store the row
        row_list = self.representation[row]
        #create a dict with the number of appearances of each number in the row
        dict_row = {i:row_list.count(i) for i in row_list}
        #store only the appearances that have more than 1 appearance(duplicates)
        num_of_duplicates_row = dict(filter(lambda val: val[1] > 1, dict_row.items()))
        #sum all the appearances of duplicates
        fitness += sum(num_of_duplicates_row.values())

    for column in range(0,9):
        #store the column
        column_list = [row[column] for row in self.representation]
        #create a dict with the number of appearances of each number in the column
        dict_columns = {i:row_list.count(i) for i in column_list}
        #store only the appearances that have more than 1 appearance(duplicates)
        num_of_duplicates_column = dict(filter(lambda val: val[1] > 1, dict_columns.items()))
        #sum all the appearances of duplicates
        fitness += sum(num_of_duplicates_column.values())

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
            block_list.append(self.representation[i + 1][j + 2] )
            block_list.append(self.representation[i + 2][j + 1])
            block_list.append(self.representation[i + 2][j + 2])
            # create a dict with the number of appearances of each number in the block
            dict_grid = {i: block_list.count(i) for i in block_list}
            # store only the appearances that have more than 1 appearance(duplicates)
            num_of_duplicates_grid = dict(filter(lambda val: val[1] > 1, dict_grid.items()))
            # sum all the appearances of duplicates
            fitness += sum(num_of_duplicates_grid.values())

        if fitness != 0:
            max_fitness = 1/fitness
        else:
            max_fitness = 1

    return  fitness


# Monkey patching
Individual.get_fitness = get_fitness
'''Individual.get_neighbours = get_neighbours'''


pop = Population(
    size= 1000,
    optim="min",
)

pop.evolve(
    gens=1000,
    select=tournament,
    crossover=new_pmx_co,
    mutate=swap_row_mutation,
    co_p=0.95,
    mu_p=0.05,
    elitism=True
)
