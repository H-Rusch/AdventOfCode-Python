def part1(input):
    door_public_key, card_public_key = parse(input)

    card_loop_size = transform(card_public_key)

    return calculate_encryption_key(card_loop_size, door_public_key)


def part2(_):
    return "🤶 No seconds puzzle on the last day (: 🤶"


def transform(target_value: int):
    value = 1
    loop_size = 0
    while value != target_value:
        value *= 7
        value = value % 20201227
        loop_size += 1
    return loop_size


def calculate_encryption_key(loop_size: int, subject_number: int):
    value = 1
    for i in range(loop_size):
        value *= subject_number
        value = value % 20201227
    return value


def parse(input):
    return (int(i) for i in input.splitlines())
