def part1(input: str) -> int:
    current_sum = 0
    for i1, i2 in zip(input, input[1:] + input[0]):
        if i1 == i2:
            current_sum += int(i1)

    return current_sum


def part2(input: str):
    current_sum = 0
    half = int(len(input) / 2)

    for i1, i2 in zip(input, input[half:] + input[:half]):
        if i1 == i2:
            current_sum += int(i1)

    return current_sum
