# Released to students

import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
from student_utils import *
import input_validator


def validate_output(input_file, output_file, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    output_data = utils.read_file(output_file)

    input_message, input_error = input_validator.tests(input_file)
    cost, message = tests(input_data, output_data, params=params)
    message = 'Comments about input file:\n\n' + input_message + 'Comments about output file:\n\n' + message

    print(message)
    if input_error:
        return input_error, 'infinite', input_message + 'Since this input is invalid, you will not receive a score for its output.\n'
    return input_error, cost, message


def validate_all_outputs(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, '.in')
    output_files = utils.get_files_with_extension(output_directory, '.out')

    all_results = []
    for input_file in input_files:
        output_file = utils.input_to_output(input_file, output_directory)
        print(input_file, output_file)
        if output_file not in output_files:
            print(f'No corresponding .out file for {input_file}')
            results = (None, None, f'No corresponding .out file for {input_file}')
        else:
            results = validate_output(input_file, output_file, params=params)

        all_results.append((input_file, results))
    return all_results


def tests(input_data, output_data, params=[]):
    number_of_locations, number_of_houses, list_of_locations, list_of_houses, starting_location, adjacency_matrix = data_parser(input_data)
    try:
        G, message = adjacency_matrix_to_graph(adjacency_matrix)
    except Exception:
        return 'Your adjacency matrix is not well formed.\n', 'infinite'
    message = ''
    cost = -1
    car_cycle = output_data[0]
    num_dropoffs = int(output_data[1][0])
    if len(output_data) - 2 != num_dropoffs:
        message += f'Number of dropoffs in output ({len(output_data) - 2}) does not match number stated ({num_dropoffs}).\n'
        cost = 'infinite'
        return cost, message
    targets = []
    dropoffs = {}
    for i in range(num_dropoffs):
        dropoff = output_data[i + 2]
        if dropoff[0] not in list_of_locations:
            message += 'At least one dropoff location is not an actual location.\n'
            cost = 'infinite'
        if dropoff[0] not in car_cycle:
            message += 'At least one dropoff location is not in the path of the car.\n'
            cost = 'infinite'
        dropoff_index = list_of_locations.index(dropoff[0])
        if list_of_locations.index(dropoff[0]) in dropoffs.keys():
            message += 'You have multiple dropoffs with the same location. Please compress them so that there is one dropoff'
            cost = 'infinite'
        dropoffs[dropoff_index] = convert_locations_to_indices(dropoff[1:], list_of_locations)
        if len(dropoff) == 1:
            message += 'One dropoff location has nobody getting off; it should not be included in the list of dropoffs.\n'
            cost = 'infinite'
        for target in dropoff[1:]:
            if target not in list_of_houses:
                message += 'One of the targets is not a house.\n'
                cost = 'infinite'
            if target in targets:
                message += 'One of the targets got off at multiple dropoffs'
                cost = 'infinite'
            targets.append(target)

    if any(target not in list_of_locations for target in targets):
        message += 'At least one of the targets is not a valid location.\n'
        cost = 'infinite'

    if any(home not in targets for home in list_of_houses):
        message += 'At least one student did not get home.\n'
        cost = 'infinite'

    if (car_cycle[0] != starting_location):
        message += "Your car must start at the specified starting location.\n"
        cost = 'infinite'

    car_cycle = convert_locations_to_indices(car_cycle, list_of_locations)

    if (car_cycle[0] != car_cycle[-1]):
        message += "Your car must start and end at the same location.\n"
        cost = 'infinite'

    if cost != 'infinite':
        cost, solution_message = cost_of_solution(G, car_cycle, dropoffs)
        message += solution_message

    return cost, message


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the output validator is run on all files in the output directory. Else, it is run on just the given output file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output', type=str, help='The path to the output file or directory')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    if args.all:
        input_directory, output_directory = args.input, args.output
        validate_all_outputs(input_directory, output_directory, params=args.params)
    else:
        input_file, output_file = args.input, args.output
        validate_output(input_file, output_file, params=args.params)
