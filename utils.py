import sys, os

def get_files_with_extension(directory, extension):
    files = []
    for name in os.listdir(directory):
        if name.endswith(extension):
            files.append(f'{directory}/{name}')
    return files


def read_file(file):
    with open(file, 'r') as f:
        data = f.readlines()
    data = [line.replace("Â", " ").strip().split() for line in data]
    return data


def write_to_file(file, string, append=False):
    if append:
        mode = 'a'
    else:
        mode = 'w'
    with open(file, mode) as f:
        f.write(string)


def write_data_to_file(file, data, separator, append=False):
    if append:
        mode = 'a'
    else:
        mode = 'w'
    with open(file, mode) as f:
        for item in data:
            f.write(f'{item}{separator}')


def input_to_output(input_file, output_directory):
    return (
        os.path.join(output_directory, os.path.basename(input_file))
        .replace("input", "output")
        .replace(".in", ".out")
    )
