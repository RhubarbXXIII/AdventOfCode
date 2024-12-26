import inspect
import os
import re


def read_file(filename: str):
    calling_file_path_directories = inspect.stack()[1].filename.split(os.path.sep)
    year = calling_file_path_directories[-2]
    day = calling_file_path_directories[-1].split('.')[0]
    with open(f"../input/{year}/{day}/{filename}", 'r') as file:
        for line in file.readlines():
            yield line


def parse(line: str, separator: str = ' ') -> list[str]:
    line = line.replace('\n', '')
    return line.split(separator) if separator != '' else list(line)


def parse_number(string: str) -> int:
    return int(re.sub(r'\D+', '', string))
