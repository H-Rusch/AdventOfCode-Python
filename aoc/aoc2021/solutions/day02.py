from aoc.util.direction import Direction


def part1(input: str) -> int:
    def get_direction(instruction: str) -> Direction:
        match instruction:
            case "forward":
                return Direction.RIGHT
            case "up" | "down":
                return Direction.from_str(instruction)

    position = (0, 0)
    for instruction, amount in parse(input):
        position = get_direction(instruction).steps(position, amount)

    return position[0] * position[1]


def part2(input: str) -> int:
    horizontal = 0
    vertical = 0
    aim = 0

    for instruction, amount in parse(input):
        if instruction == "up":
            aim -= amount
        elif instruction == "down":
            aim += amount
        else:
            horizontal += amount
            vertical += aim * amount

    return horizontal * vertical


def parse(input: str) -> list[tuple[str, int]]:
    return [(line.split()[0], int(line.split()[1])) for line in input.splitlines()]
