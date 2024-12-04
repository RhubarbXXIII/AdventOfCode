import inspect
import os.path


DIRECTIONS = (-1, 0, 1)


def read_file(filename: str):
    calling_file_path_directories = inspect.stack()[1].filename.split(os.path.sep)
    year = calling_file_path_directories[-2]
    day = calling_file_path_directories[-1].split('.')[0]
    with open(f"../input/{year}/{day}/{filename}", 'r') as file:
        for line in file.readlines():
            yield line

def parse(line: str, separator: str = ' ') -> list[str]:
    return line.replace('\n', '').split(separator)