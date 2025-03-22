def part1(input):
    numbers = parse(input)

    return get_most_recent_at_n(numbers, 2020)


def part2(input):
    numbers = parse(input)

    return get_most_recent_at_n(numbers, 300_000_00)


def get_most_recent_at_n(numbers, n):
    memory = {numbers[i]: i + 1 for i in range(len(numbers) - 1)}

    most_recently = numbers[-1]
    current_count = len(numbers)

    while True:
        if current_count == n:
            return most_recently

        if most_recently not in memory.keys():
            memory[most_recently] = current_count
            most_recently = 0
        else:
            z = current_count - memory[most_recently]
            memory[most_recently] = current_count
            most_recently = z

        current_count += 1


def parse(input):
    return [int(n) for n in input.split(",")]
