import os
import json
import argparse

"""
Run `python3 compress_outputs.py <path to output folder>` and submit the 'outputs.json'
that is created to gradescope.
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('outputs', type=str, help='The path to the output file or directory')
    args = parser.parse_args()
    with open('outputs.json', 'w') as output_json:
        data = {}
        for output in os.listdir(args.outputs):
            with open(args.outputs + output, 'r') as output_file:
                if output[-4:] == '.out':
                    string = ''
                    for l in output_file.readlines():
                        string += l
                        data[output] = string
        output_json.write(json.dumps(data))
