from random import shuffle, choice, sample, random
from operator import attrgetter
from copy import deepcopy
import numpy

'''Load the sudoku initial values (sudoku_data.txt) into a variable'''
with open('sudoku_data.txt') as f:
    initial_data = numpy.loadtxt(f).reshape((9, 9)).astype(int)

    #pencil mark method
    def pencil_mark(i,j):
        pencil_list = [1,2,3,4,5,6,7,8,9]

        #Get values from the same row and remove from pencil_list
        for column in range(0,9):
            if (initial_data[i][column] != 0 and initial_data[i][column] in pencil_list):
                pencil_list.remove(initial_data[i][column])

        #Get values from the same column and remove from pencil_list
        for row in range(0, 9):
            if (initial_data[row][j] != 0 and initial_data[row][j] in pencil_list):
                pencil_list.remove(initial_data[row][j])

        #Get values from the same grid (3x3) and remove from pencil_list
        for a in range(0, 9, 3):
            for b in range(0, 9, 3):
                #if i,j are between...
                if (i >= a and i <= a + 2):
                    if (j >= b and j <= b + 2):
                        #then find the values from that grid
                        for k in find_grid(a, b):
                            if (k != 0 and k in pencil_list):
                                pencil_list.remove(k)

        return pencil_list

    #returns the values of a grid
    def find_grid(i,j):
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
        initial_set=initial_data
    ):
        if representation is None:
            self.representation= [[[] for j in range(0, 9)] for i in range(0, 9)]
            for row in range(0, 9):
                for column in range(0, 9):
                    if initial_set[row][column] == 0:
                        # Value is available.
                            self.representation[row][column] = choice(pencil_mark(row,column))
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


class Population:
    def __init__(self, size, optim, **kwargs):
        self.individuals = []
        self.size = size
        self.optim = optim


        for _ in range(size):
            self.individuals.append(
                Individual()
            )

    def evolve(self, gens, select, crossover, mutate, co_p, mu_p, elitism):


        for gen in range(gens):
            new_pop = []

            if elitism == True:
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
                if random() < mu_p:
                    offspring1 = mutate(offspring1)
                if random() < mu_p:
                    offspring2 = mutate(offspring2)

                new_pop.append(Individual(representation=offspring1))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))

            if elitism == True:
                if self.optim == "max":
                    least = min(new_pop, key=attrgetter("fitness"))
                elif self.optim == "min":
                    least = max(new_pop, key=attrgetter("fitness"))
                new_pop.pop(new_pop.index(least))
                new_pop.append(elite)

            self.individuals = new_pop

            if self.optim == "max":
                print(f'Gen {gen}' + " - " + f'Best Individual: {max(self, key=attrgetter("fitness"))}')
            elif self.optim == "min":
                print(f'Gen {gen}' + " - " + f'Best Individual: {min(self, key=attrgetter("fitness"))}')

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)}, individual_size={len(self.individuals[0])})"
