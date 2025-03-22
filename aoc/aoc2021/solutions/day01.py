def part1(input: str) -> int:
    numbers = parse(input)
    times_increasing = 0

    for i in range(1, len(numbers)):
        if numbers[i - 1] < numbers[i]:
            times_increasing += 1

    return times_increasing


def part2(input: str) -> int:
    numbers = parse(input)
    times_increasing = 0

    for i in range(3, len(numbers)):
        if sum(numbers[i - 4 : i - 1]) < sum(numbers[i - 3 : i]):
            times_increasing += 1

    return times_increasing


def parse(input: str):
    return [int(s) for s in input.splitlines()]
