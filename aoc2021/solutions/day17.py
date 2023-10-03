import re


def part1(input: str) -> int:
    _, _, y0, _ = parse(input)

    return y0 * (y0 + 1) // 2


def part2(input: str) -> int:
    x0, x1, y0, y1 = parse(input)

    velocities = set()
    for x_velocity in range(x1 + 1):
        for y_velocity in range(y0, abs(y0) + 1):
            if falls_into_target(x_velocity, y_velocity, x0, x1, y0, y1):
                velocities.add((x_velocity, y_velocity))

    return len(velocities)


def falls_into_target(start_x: int, start_y: int, x0: int, x1: int, y0: int, y1: int) -> bool:
    x, y = 0, 0

    momentum_x, momentum_y = start_x, start_y
    while True:
        x += momentum_x
        y += momentum_y

        if momentum_x > 0:
            momentum_x -= 1
        momentum_y -= 1

        if x in range(x0, x1 + 1) and y in range(y0, y1 + 1):
            return True

        if y < y0:
            return False


def parse(input: str):
    return [int(n) for n in re.findall(r"-?\d+", input)]
