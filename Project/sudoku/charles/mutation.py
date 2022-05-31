from random import randint, sample
import numpy as np

'''

Load the initial data from the file "sudoku_data.txt"

'''

with open('charles\sudoku_data.txt') as f:
    initial_data = np.loadtxt(f).reshape((9, 9)).astype(int)

''''

Swap two random cells from a random row  

'''

def swap_row_mutation(individual):

    # select a random row of the sudoku matrix
    mut_row = sample(range(len(individual)), 1)
    # select 2 random indexes from that row
    mut_points = sample(range(len(individual[mut_row[0]])), 2)

    # store the indexes of the initial sudoku set where the value is not 0 (unchangeable values)
    index_list = [i for i, e in enumerate(initial_data[mut_row[0]]) if e != 0]

    # if one of the mutation points is an unchangeable  value, sample again
    while ((mut_points[0] in index_list) or (mut_points[1] in index_list)):
        mut_points = sample(range(len(individual[mut_row[0]])), 2)

    # This method assumes that the second point is after (on the right of) the first one
    # Sort the list
    mut_points.sort()
    #Swap
    individual[mut_row[0]][mut_points[0]], individual[mut_row[0]][mut_points[1]] = individual[mut_row[0]][mut_points[1]], individual[mut_row[0]][mut_points[0]]

    return individual


''''

Swap two random cells from a random column  

'''

def swap_column_mutation(individual):

    # Position of the start and end of substring

    # select a random column of the sudoku matrix
    mut_column = sample(range(len(individual)), 1)
    # select 2 random points from that column
    mut_points = sample(range(len(individual)), 2)
    # store the indexes of the initial sudoku set where the value is not 0 (unchangeable values)
    index_list = [i for i, e in enumerate([row[mut_column[0]] for row in initial_data]) if e != 0]

    # Invert for the mutation
    # if one of the mutation points is an unchangeable  value, sample again
    while ((mut_points[0] in index_list) or (mut_points[1] in index_list)):
        mut_points = sample(range(len(individual)), 2)

    # This method assumes that the second point is after (on the right of) the first one
    # Sort the list
    mut_points.sort()
    #Swap
    individual[mut_points[0]][mut_column[0]], individual[mut_points[1]][mut_column[0]] = individual[mut_points[1]][mut_column[0]], individual[mut_points[0]][mut_column[0]]

    return individual


''''

Swap two random cells from a random grid  

'''

def swap_grid_mutation(individual):

    individual = np.array(individual).reshape((9, 9))
    #choose grid row
    grid_row = sample([0,3,6],1)
    #choose grid column
    grid_column = sample([0,3,6],1)

    #randomly choose mutation points
    mut_points_1 = np.random.choice([0, 1, 2], size=2, replace=True)
    mut_points_2 = np.random.choice([0, 1, 2], size=2, replace=True)

    #while the value at mutation points 1 or mutation points 2 is a fixed value, or mutation points 1 equals mutation points 2, resample:
    while(((individual[grid_row[0] + mut_points_1[0]][grid_column[0] + mut_points_1[1]]) == (initial_data[grid_row[0] + mut_points_1[0]][grid_column[0] + mut_points_1[1]]))
        | ((individual[grid_row[0] + mut_points_2[0]][grid_column[0] + mut_points_2[1]]) == (initial_data[grid_row[0] + mut_points_2[0]][grid_column[0] + mut_points_2[1]]))
        | (mut_points_1 == mut_points_2).all()):
        mut_points_1 = np.random.choice([0, 1, 2], size=2, replace=True)
        mut_points_2 = np.random.choice([0, 1, 2], size=2, replace=True)

    #swap values at mutation points 1 and 2
    temp = individual[grid_row[0] + mut_points_1[0]][grid_column[0] + mut_points_1[1]]
    individual[grid_row[0] + mut_points_1[0]][grid_column[0] + mut_points_1[1]] = individual[grid_row[0] + mut_points_2[0]][grid_column[0] + mut_points_2[1]]
    individual[grid_row[0] + mut_points_2[0]][grid_column[0] + mut_points_2[1]] = temp


    return individual.tolist()

''''

Choose a random cell and change its value to a random integer from 1 to 9
'''


def random_mutation(individual):

    individual = np.array(individual).flatten(order='C').tolist()
    initial_set = np.array(initial_data).flatten(order='C').tolist()

    #select a random index
    mut_index = sample(range(len(initial_set)), 1)

    # store the indexes of the initial sudoku set where the value is not 0 (unchangeable values)
    index_list = [i for i, e in enumerate(initial_set) if e != 0]

    #if the chosen cell is a fixed value change cell
    while (mut_index[0] in index_list):
        mut_index = sample(range(len(initial_set)), 1)

    #get a random value from [1,9]
    value = randint(1,9)

    #if the cell = value, change value
    while (value == individual[mut_index[0]]):
        value = randint(1, 9)

    #change the cell to the random value
    individual[mut_index[0]] = value

    return np.array(individual).reshape((9, 9)).astype(int).tolist()


def inversion_mutation(individual):
    """Inversion mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """


    #select a random row of the sudoku matrix
    mut_row = sample(range(len(individual)), 1)
    #select 2 random points from that row
    mut_points = sample(range(len(individual[mut_row[0]])), 2)

    # store the indexes of the initial sudoku set where the value is not 0 (unchangeable values)
    index_list = [i for i, e in enumerate(initial_data[mut_row[0]]) if e != 0]

    #if one of the mutation points is an unchangeable  value, sample again
    while ((mut_points[0] in index_list) or (mut_points[1] in index_list)):
        mut_points = sample(range(len(individual[mut_row[0]])), 2)

    # This method assumes that the second point is after (on the right of) the first one
    # Sort the list
    mut_points.sort()

    individual[mut_row[0]][mut_points[0]:mut_points[1]] = individual[mut_row[0]][mut_points[0]:mut_points[1]][::-1]

    return individual


if __name__ == '__main__':
   ''' test = [6, 1, 3, 5, 2, 4, 7]
    index_list = [i for i, e in enumerate(initial_data[0]) if e != 0]
    mut_points = sample(range(len(initial_data[0])), 2)
    mut_row = sample(range(len(initial_data)), 1)
    print(index_list)
    print(mut_row)
    print(mut_points[0] in index_list)'''

