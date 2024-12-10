from collections import defaultdict

from utils import read_file


def parse_file(filename: str) -> list[int]:
    disk_map: list[int] = []
    for line in read_file(filename):
        disk_map = list(map(int, line))

    return disk_map


def part1() -> int:
    disk_map = parse_file("input.txt")

    front_disk_map_index = 0
    front_file_id = 0
    front_remaining_block_count = disk_map[front_disk_map_index]
    back_disk_map_index = len(disk_map) - 1
    back_file_id = back_disk_map_index // 2
    back_remaining_block_count = disk_map[back_disk_map_index]

    disk_index = 0

    checksum = 0
    while front_disk_map_index <= back_disk_map_index:
        if front_file_id == back_file_id:
            front_remaining_block_count = min(front_remaining_block_count, back_remaining_block_count)
            back_remaining_block_count = front_remaining_block_count

        if front_disk_map_index % 2 == 0:
            checksum += disk_index * front_file_id
            front_remaining_block_count -= 1
        else:
            checksum += disk_index * back_file_id
            front_remaining_block_count -= 1
            back_remaining_block_count -= 1

        disk_index += 1

        while front_remaining_block_count == 0:
            front_disk_map_index += 1
            front_remaining_block_count = disk_map[front_disk_map_index]
            if front_disk_map_index % 2 == 0:
                front_file_id += 1

        if back_remaining_block_count == 0:
            back_disk_map_index -= 2
            back_remaining_block_count = disk_map[back_disk_map_index]
            back_file_id -= 1

    return checksum


def part2() -> int:
    disk_map = parse_file("input.txt")

    disk_index = 0

    empty_blocks: dict[int, list[int]] = defaultdict(list)
    for disk_map_index, block_size in enumerate(disk_map):
        if disk_map_index % 2 == 1:
            empty_blocks[block_size].append(disk_index)

        disk_index += block_size

    file_id = (len(disk_map) - 1) // 2
    checksum = 0

    for disk_map_index, block_size in enumerate(disk_map[::-1]):
        disk_index -= block_size

        if disk_map_index % 2 == 0:
            selected_disk_index = None
            selected_empty_block_size = None
            for empty_block_size in range(block_size, 10):
                if not empty_blocks[empty_block_size]:
                    continue

                if empty_blocks[empty_block_size][0] > disk_index:
                    continue

                if selected_disk_index is None or empty_blocks[empty_block_size][0] < selected_disk_index:
                    selected_disk_index = empty_blocks[empty_block_size][0]
                    selected_empty_block_size = empty_block_size

            if selected_disk_index is not None:
                new_disk_index = selected_disk_index
                empty_block_size = selected_empty_block_size

                for block_index in range(block_size):
                    checksum += (new_disk_index + block_index) * file_id

                empty_blocks[empty_block_size].pop(0)

                remaining_empty_block_disk_index = new_disk_index + block_size
                new_empty_block_size = empty_block_size - block_size

                inserted = False
                for empty_block_index, empty_block_disk_index in enumerate(empty_blocks[new_empty_block_size]):
                    if remaining_empty_block_disk_index < empty_block_disk_index:
                        empty_blocks[new_empty_block_size].insert(empty_block_index, remaining_empty_block_disk_index)
                        inserted = True
                        break

                if not inserted:
                    empty_blocks[new_empty_block_size].append(remaining_empty_block_disk_index)

            else:
                for block_index in range(block_size):
                    checksum += (disk_index + block_index) * file_id

            file_id -= 1

    return checksum


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
