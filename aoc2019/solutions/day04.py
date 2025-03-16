def part1(input) -> int:
    start, stop = parse(input)

    count = 0
    for i in range(start, stop):
        if check_valid_password(i):
            count += 1

    return count


def part2(input) -> int:
    start, stop = parse(input)

    count = 0
    for i in range(start, stop):
        if check_valid_password_part2(i):
            count += 1

    return count


def check_valid_password(password: int) -> bool:
    digits = [d for d in str(password)]
    same_adjacent = False
    for i in range(len(digits) - 1):
        if digits[i] == digits[i + 1]:
            same_adjacent = True
        elif digits[i] > digits[i + 1]:
            # digits decrease from left to right
            return False

    return same_adjacent


def check_valid_password_part2(password: int) -> bool:
    digits = [d for d in str(password)]
    ab = digits[0] == digits[1]
    bc = digits[1] == digits[2]
    cd = digits[2] == digits[3]
    de = digits[3] == digits[4]
    ef = digits[4] == digits[5]

    for i in range(len(digits) - 1):
        if digits[i] > digits[i + 1]:
            # digits decrease from left to right
            return False

    # one pair of two numbers that is not in a group of more than two of the same numbers
    return (
        (ab and not bc)
        or (not ab and bc and not cd)
        or (not bc and cd and not de)
        or (not cd and de and not ef)
        or (not de and ef)
    )

    # cool alternative I found online to check if there is a pair of values next to each other which does not belong to
    # a bigger group:
    # return 2 in map(lambda n: digits.count(n), digits)


def parse(input):
    return (int(n) for n in input.split("-"))
