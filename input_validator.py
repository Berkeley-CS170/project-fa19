import sys
sys.path.append('..')
sys.path.append('../..')
import os
import argparse
import utils
import networkx as nx
import numpy as np
from student_utils import *

# Change these if you want to allow files with different names and/or graph sizes
RANGE_OF_INPUT_SIZES = [50, 100, 200]
VALID_FILENAMES = ['50.in', '100.in', '200.in']
MAX_NAME_LENGTH = 20

def validate_input(input_file, params=[]):
    print('Processing', input_file)
    message, error = tests(input_file, params)
    print(message)


def validate_all_inputs(input_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        validate_input(input_file, params=params)


def tests(input_file, params=[]):
    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    message = ''
    error = False

    file_basename = os.path.basename(input_file)

    # check name constraints
    if file_basename not in VALID_FILENAMES:
        message += f'Your file is named {file_basename}. The allowed file names are: {RANGE_OF_INPUT_SIZES}.\n'
        error = True

    for i in range(len(RANGE_OF_INPUT_SIZES)):
        if file_basename == VALID_FILENAMES[i] and (int(num_of_locations) > RANGE_OF_INPUT_SIZES[i]):
            message += f'Your file is named {file_basename}, but the size of the input is {num_of_locations}.\n'
            error = True

    if not all(name.isalnum() and len(name) <= MAX_NAME_LENGTH for name in list_locations):
        message += f'One or more of the names of your locations are either not alphanumeric or are above the max length of {MAX_NAME_LENGTH}.\n'
        error = True

    # check counts
    if len(list_locations) != num_of_locations:
        message += f'The number of locations you listed ({len(list_locations)}) differs from the number you gave on the first line ({num_of_locations}).\n'
        error = True

    if len(list_houses) != num_houses:
        message += f'The number of homes you listed ({len(list_houses)}) differs from the number you gave on the first line ({num_houses}).\n'
        error = True

    if num_of_locations < num_houses:
        message += f'The number of houses must be less than or equal to the number of locations.\n'
        error = True

    # check containment
    if any(house not in list_locations for house in list_houses):
        message += f'You listed at least one house that is not an actual location. Ahh!\n'
        error = True

    if starting_car_location not in list_locations:
        message += f'You listed a starting car location that is not an actual location.\n'
        error = True

    # check distinct
    if not len(set(list_locations)) == len(list_locations):
        message += 'The names of your locations are not distinct.\n'
        error = True

    if not len(set(list_houses)) == len(list_houses):
        message += 'The names of your houses are not distinct.\n'
        error = True

    # check adjacency matrix
    if not len(adjacency_matrix) == len(adjacency_matrix[0]) == num_of_locations:
        message += f'The dimensions of your adjacency matrix do not match the number of locations you provided.\n'
        error = True

    if not all(entry == 'x' or (type(entry) is float and entry > 0 and entry <= 2e9 and decimal_digits_check(entry)) for row in adjacency_matrix for entry in row):
        message += f'Your adjacency matrix may only contain the character "x", or strictly positive integers less than 2e+9, or strictly positive floats with less than 5 decimal digits.\n'
        error = True

    # if not square, terminate
    if len(set(map(len, adjacency_matrix))) != 1 or len(adjacency_matrix[0]) != len(adjacency_matrix):
        message += f'Your adjacency matrix must be square.\n'
        error = True
        return message, error

    adjacency_matrix_numpy = np.matrix(adjacency_matrix)

    # check requirements on square matrix
    if not np.all(adjacency_matrix_numpy.T == adjacency_matrix_numpy):
        message += f'Your adjacency matrix is not symmetric.\n'
        error = True

    G, adj_message = adjacency_matrix_to_graph(adjacency_matrix)

    # if failed to create adjacency matrix, terminate
    if adj_message:
        message += adj_message
        error = True
        return message, error

    if not nx.is_connected(G):
        message += 'Your graph is not connected.\n'
        error = True

    if not is_metric(G):
        message += 'Your graph is not metric.\n'
        error = True

    if not message:
        message = "If you've received no other error messages, then your input is valid!\n\n\n"
    return message, error


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the input validator is run on all files in the input directory. Else, it is run on just the given input file.')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    if args.all:
        input_directory = args.input
        validate_all_inputs(input_directory, params=args.params)
    else:
        input_file = args.input
        validate_input(input_file, params=args.params)
