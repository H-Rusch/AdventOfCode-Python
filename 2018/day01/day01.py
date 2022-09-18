from itertools import cycle


def part_1(changes: list) -> int:
    return sum([int(s) for s in changes])


def part_2(changes: list) -> int:
    current = 0
    seen_frequencies = {current}

    for change in cycle(changes):
        current += int(change)
        if current in seen_frequencies:
            return current
        seen_frequencies.add(current)


def parse_input() -> list:
    with open("input.txt", "r") as file:
        return file.readlines()


if __name__ == "__main__":
    values = parse_input()

    print(f"Part 1: The resulting frequency is {part_1(values)}.")

    print(f"Part 2: The first frequency which is reached twice is {part_2(values)}.")
