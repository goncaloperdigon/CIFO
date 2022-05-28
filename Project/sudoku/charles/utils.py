from matplotlib import pyplot as plt
import numpy as np
'''
def plot_c(c, alpha, threshold):
    """ A function to visualize the changing c value (vertical) and
    number of updates (horizontal)

    Args:
        c: temperature parameter
        alpha: decreasing factor
        threshold: threshold for termination condition
    """
    c_list = [c]
    while c > threshold:
        c = c * alpha
        c_list.append(c)
    plt.plot(c_list)
    plt.show()


plot_c(100, 0.8, 0.05)'''

import numpy
from random import shuffle, choice, sample, random


with open('sudoku_data.txt') as f:
    initial_data = numpy.loadtxt(f).reshape((9, 9)).astype(int)

representation = [[[] for j in range(0, 9)] for i in range(0, 9)]

for row in range(0, 9):
    for column in range(0, 9):
            if (initial_data[row][column] == 0):
                # Value is available.
                representation[row][column] = choice([1,2,3,4,5,6,7,8,9])
            elif (initial_data[row][column] != 0):
                # Given/known value from file.
                representation[row][column] = initial_data[row][column]

'''print(initial_data)
print( is_block_duplicate(initial_data,0,0,6))'''

fitness = 0

#
for row in range(0,9):
    #store the row
    row_list = representation[row]
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
    column_list = representation[column]
    #create a dict with the number of appearances of each number in the column
    my_dict = {i:row_list.count(i) for i in column_list}
    #store only the appearances that have more than 1 appearance(duplicates)
    num_of_duplicates = dict(filter(lambda val: val[1] > 1, my_dict.items()))
    #sum all the appearances of duplicates
    sum(num_of_duplicates.values())
    fitness += sum(num_of_duplicates.values())


for i in range(0, 9, 3):
    for j in range(0, 9, 3):
        #create an empty list and store all of the values of the 3x3 block
        block_list = []
        block_list.append(representation[i][j])
        block_list.append(representation[i][j+1])
        block_list.append(representation[i][j+2])
        block_list.append(representation[i+1][j])
        block_list.append(representation[i+2][j])
        block_list.append(representation[i+1][j+1])
        block_list.append(representation[i+1][j]+2)
        block_list.append(representation[i+2][j+1])
        block_list.append(representation[i+2][j+2])

        # create a dict with the number of appearances of each number in the block
        my_dict = {i: block_list.count(i) for i in column_list}
        # store only the appearances that have more than 1 appearance(duplicates)
        num_of_duplicates = dict(filter(lambda val: val[1] > 1, my_dict.items()))
        # sum all the appearances of duplicates
        sum(num_of_duplicates.values())
        fitness += sum(num_of_duplicates.values())
x = [[4, 3, 9, 2, 7, 8, 6, 5, 1], [5, 8, 4, 1, 4, 6, 7, 2, 9], [6, 2, 1, 5, 6, 9, 4, 8, 3], [1, 9, 3, 2, 5, 8, 7, 6, 4], [6, 5, 8, 4, 3, 2, 9, 1, 7], [2, 4, 7, 7, 1, 9, 5, 3, 8], [4, 5, 2, 7, 4, 1, 8, 9, 3], [9, 7, 4, 3, 8, 5, 6, 1, 2], [3, 1, 8, 6, 2, 9, 5, 7, 4]]
x = np.reshape(x,(9, 9))
print(x)
