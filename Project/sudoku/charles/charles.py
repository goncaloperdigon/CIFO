from random import shuffle, choice, sample, random
from operator import attrgetter
from copy import deepcopy
import numpy
import time as t

'''Load the sudoku initial values (sudoku_data.txt) into a variable'''
with open('charles\sudoku_data.txt') as f:
    initial_data = numpy.loadtxt(f).reshape((9, 9)).astype(int)


    # pencil mark method
    def pencil_mark(i, j):
        pencil_list = [i for i in range(1,10)]

        # Get values from the same row and remove from pencil_list
        for column in range(0, 9):
            if initial_data[i][column] != 0 and initial_data[i][column] in pencil_list:
                pencil_list.remove(initial_data[i][column])

        # Get values from the same column and remove from pencil_list
        for row in range(0, 9):
            if initial_data[row][j] != 0 and initial_data[row][j] in pencil_list:
                pencil_list.remove(initial_data[row][j])

        # Get values from the same grid (3x3) and remove from pencil_list
        for a in range(0, 9, 3):
            for b in range(0, 9, 3):
                # if i,j are between...
                if (i >= a and i <= a + 2):
                    if (j >= b and j <= b + 2):
                        # then find the values from that grid
                        for k in find_grid(a, b):
                            if (k != 0 and k in pencil_list):
                                pencil_list.remove(k)

        return pencil_list


    # returns the values of a grid
    def find_grid(i, j):
        grid_list = []

        grid_list.append(initial_data[i][j])
        grid_list.append(initial_data[i][j + 1])
        grid_list.append(initial_data[i][j + 2])
        grid_list.append(initial_data[i + 1][j])
        grid_list.append(initial_data[i + 2][j])
        grid_list.append(initial_data[i + 1][j + 1])
        grid_list.append(initial_data[i + 1][j + 2])
        grid_list.append(initial_data[i + 2][j + 1])
        grid_list.append(initial_data[i + 2][j + 2])

        return grid_list


class Individual:
    def __init__(
            self,
            representation=None,
            initial_set=initial_data,
            optim=None
    ):
        self.optim = optim

        if representation is None:
            #create representation as an empty 9x9 matrix
            self.representation = [[[] for j in range(0, 9)] for i in range(0, 9)]
            #loop through the values of the initial sudoku set
            for row in range(0, 9):
                for column in range(0, 9):
                    if initial_set[row][column] == 0:
                        # Value is available.
                        self.representation[row][column] = choice(pencil_mark(row, column))
                    elif initial_set[row][column] != 0:
                        # Given/known value from file.
                        self.representation[row][column] = initial_set[row][column]
        else:
            self.representation = representation

        self.fitness = self.get_fitness()

    def get_fitness(self):
        raise Exception("You need to monkey patch the fitness path.")

    def get_neighbours(self, func, **kwargs):
        raise Exception("You need to monkey patch the neighbourhood function.")

    def index(self, value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f"Individual(size={len(self.representation)}); Fitness: {self.fitness}"

    #returns representation as a 9x9 matrix
    def rep_matrix(self):
        return f"Solution: \n {numpy.array(self.representation).reshape((9, 9))}"






class Population:
    def __init__(self, size, optim,last_gen, time_taken):
        self.individuals = []
        self.size = size
        self.optim = optim
        self.last_gen = last_gen
        self.time_taken = time_taken


        for _ in range(size):
            self.individuals.append(
                Individual(
                    optim = optim
                )
            )

    def evolve(self, gens, select, crossover, mutate, co_p, mu_p, elitism):

        start = t.time()

        for gen in range(gens):
            new_pop = []

            if elitism:
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))

            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)
                # Crossover
                if random() < co_p:
                    offspring1, offspring2 = crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2
                # Mutation
                #if (min(self, key=attrgetter("fitness")).fitness < 10):
                 #   mu_p = 0.5
                if random() < mu_p:
                    offspring1 = mutate(offspring1)
                if random() < mu_p:
                    offspring2 = mutate(offspring2)

                new_pop.append(Individual(representation=offspring1,optim = self.optim))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2,optim = self.optim))

            if elitism:
                if self.optim == "max":
                    least = min(new_pop, key=attrgetter("fitness"))
                elif self.optim == "min":
                    least = max(new_pop, key=attrgetter("fitness"))
                new_pop.pop(new_pop.index(least))
                new_pop.append(elite)

            self.individuals = new_pop

            if self.optim == "max":
                fit_value = max(self, key=attrgetter("fitness"))
                if (fit_value.fitness == 1):
                    self.last_gen = gen
                    self.time_taken = t.time() - start
                    print('Reached global optimum - ' + f'Gen {gen}' + " - " + f'Best Individual: {max(self, key=attrgetter("fitness"))}')
                    print(fit_value.rep_matrix())
                    print(f'Time taken:{round(self.time_taken,4)} seconds')
                    break
                else:
                    print(f'Gen {gen}' + " - " + f'Best Individual: {max(self, key=attrgetter("fitness"))}')
            elif self.optim == "min":
                fit_value = min(self, key=attrgetter("fitness"))
                if (fit_value.fitness == 0):
                    self.last_gen = gen
                    self.time_taken = t.time() - start
                    print('Reached global optimum - ' + f'Gen {gen}' + " - " + f'Best Individual: {min(self, key=attrgetter("fitness"))}')
                    print(fit_value.rep_matrix())
                    print(f'Time taken: {round(self.time_taken,4)} seconds')
                    break
                else:
                    print(f'Gen {gen}' + " - " + f'Best Individual: {min(self, key=attrgetter("fitness"))}')

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)}, individual_size={len(self.individuals[0])})"
