def part1(input: str) -> int:
    horizontal = 0
    vertical = 0

    for instruction in input.splitlines():
        direction, number = instruction.split()

        if direction == "up":
            vertical -= int(number)
        elif direction == "down":
            vertical += int(number)
        else:
            horizontal += int(number)

    return horizontal * vertical


def part2(input: str) -> int:
    horizontal = 0
    vertical = 0
    aim = 0

    for instruction in input.splitlines():
        direction, number = instruction.split()

        if direction == "up":
            aim -= int(number)
        elif direction == "down":
            aim += int(number)
        else:
            horizontal += int(number)
            vertical += aim * int(number)

    return horizontal * vertical
