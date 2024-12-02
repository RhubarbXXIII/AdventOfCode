def read_file(filename: str):
    with open(filename, 'r') as file:
        for line in file.readlines():
            yield line

def parse(line: str, separator: str = ' ') -> list[str]:
    return line.replace('\n', '').split(separator)