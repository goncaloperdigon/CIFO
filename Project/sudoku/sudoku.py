from charles.charles import Population, Individual
from copy import deepcopy
from charles.selection import fps, tournament , ranking
from charles.mutation import swap_row_mutation, inversion_mutation, swap_column_mutation, random_mutation, swap_grid_mutation
from charles.crossover import  new_pmx_co, row_crossover, uniform_crossover, single_point_co
import numpy
import time

"""
    Fitness function - counts the number of duplicates in entire sudoku matrix
    NOTE: We count a pair of duplicates as 2 duplicates. E.g. If there is two 1's in a row, that row has 2 duplicates
    
"""

def get_fitness(self):

    fitness = 0

    #calculate number of duplicates in all rows

    for row in range(0,9):
        #store the row
        row_list = self.representation[row]
        #create a dict with the number of appearances of each number in the row
        dict_row = {i:row_list.count(i) for i in row_list}
        #store only the appearances that have more than 1 appearance(duplicates)
        num_of_duplicates_row = dict(filter(lambda val: val[1] > 1, dict_row.items()))
        #sum all the appearances of duplicates
        fitness += sum(num_of_duplicates_row.values())

    # calculate number of duplicates in all columns
    for column in range(0,9):
        #store the column
        column_list = [row[column] for row in self.representation]
        #create a dict with the number of appearances of each number in the column
        dict_columns = {i:column_list.count(i) for i in column_list}
        #store only the appearances that have more than 1 appearance(duplicates)
        num_of_duplicates_column = dict(filter(lambda val: val[1] > 1, dict_columns.items()))
        #sum all the appearances of duplicates
        fitness += sum(num_of_duplicates_column.values())

    # calculate number of duplicates in all grids
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
            block_list.append(self.representation[i + 1][j + 2])
            block_list.append(self.representation[i + 2][j + 1])
            block_list.append(self.representation[i + 2][j + 2])
            # create a dict with the number of appearances of each number in the block
            dict_grid = {i: block_list.count(i) for i in block_list}
            # store only the appearances that have more than 1 appearance(duplicates)
            num_of_duplicates_grid = dict(filter(lambda val: val[1] > 1, dict_grid.items()))
            # sum all the appearances of duplicates
            fitness += sum(num_of_duplicates_grid.values())

    #if optimization = maximization, the fitness function changes to 1/#duplicates
    if (self.optim=="max"):
        if fitness != 0:
            fitness = 1/fitness
        #when fitness = 0, we have found a solution, return 1 to not divide by 0
        else:
            fitness = 1

    return fitness


# Monkey patching
Individual.get_fitness = get_fitness

#Performance parameters
time = []
number_gens = []
failed_runs = 0

#Change if more than 1 run needed (specify number in range of the for loop)
for _ in range(1):
    pop = Population(
        size= 1000,
        optim="min",
        last_gen=0,
        time_taken=0
    )

    pop.evolve(
        gens= 1000,
        select= ranking,
        crossover = new_pmx_co,
        mutate = swap_grid_mutation,
        co_p=0.9,
        mu_p=0.1,
        elitism = True
    )
    if pop.last_gen != 0:
        number_gens.append(pop.last_gen)
        time.append(pop.time_taken)
    else: failed_runs += 1

#Print performance metrics
print(f'Average time: {round(numpy.average(time),3)}')
print(f'Average number of gens: {int(numpy.average(number_gens))}')
print(f'Failed runs: {failed_runs}')
