FACTOR_A = 16_807
FACTOR_B = 48_271
DIVISOR = 2_147_483_647
LIMIT = 40_000_000
LIMIT2 = 5_000_000


def part1(input):
    init_a, init_b = parse(input)
    a_values = value_generator(init_a, FACTOR_A)
    b_values = value_generator(init_b, FACTOR_A)

    return count_matching_numbers(a_values, b_values, LIMIT)


def part2(input):
    init_a, init_b = parse(input)
    a_values = divisible_by(value_generator(init_a, FACTOR_A), 4)
    b_values = divisible_by(value_generator(init_b, FACTOR_B), 8)

    return count_matching_numbers(a_values, b_values, LIMIT2)


def count_matching_numbers(a_values, b_values, limit: int) -> int:
    count = 0
    for _ in range(limit):
        a = next(a_values)
        b = next(b_values)

        # get the lower 16 bits by computing logical and
        a16 = a & 0xFFFF
        b16 = b & 0xFFFF

        if a16 == b16:
            count += 1

    return count


def value_generator(initial: int, factor: int):
    value = initial
    while True:
        yield value
        value = (value * factor) % DIVISOR


def divisible_by(numbers, d: int):
    for number in numbers:
        if number % d == 0:
            yield number


def parse(input) -> (int, int):
    return (int(line.split()[-1]) for line in input.splitlines())
