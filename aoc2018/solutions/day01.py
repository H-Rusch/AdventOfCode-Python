from itertools import cycle


def part1(input: str) -> int:
    changes = parse(input)

    return sum([int(s) for s in changes])


def part2(input: str) -> int:
    changes = parse(input)

    current = 0
    seen_frequencies = {current}

    for change in cycle(changes):
        current += int(change)
        if current in seen_frequencies:
            return current
        seen_frequencies.add(current)


def parse(input) -> list:
    return input.splitlines()
