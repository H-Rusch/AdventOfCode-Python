FACTOR_A = 16_807
FACTOR_B = 48_271
DIVISOR = 2_147_483_647
LIMIT = 40_000_000
LIMIT2 = 5_000_000


def part1(input):
    init_a, init_b = parse(input)
    a_values = generator_a(init_a)
    b_values = generator_b(init_b)

    return count_matching_numbers(a_values, b_values, LIMIT)


def part2(input):
    init_a, init_b = parse(input)
    a_values = divisible_by(generator_a(init_a), 4)
    b_values = divisible_by(generator_b(init_b), 8)

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


def generator_a(initial_a: int):
    a = initial_a
    while True:
        yield a
        a = (a * FACTOR_A) % DIVISOR


def generator_b(initial_b: int):
    b = initial_b
    while True:
        yield b
        b = (b * FACTOR_B) % DIVISOR


def divisible_by(numbers, d: int):
    for number in numbers:
        if number % d == 0:
            yield number


def parse(input) -> (int, int):
    return (int(line.split()[-1]) for line in input.splitlines())
