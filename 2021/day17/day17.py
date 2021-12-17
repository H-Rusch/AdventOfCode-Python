import re


def part_1(y0: int) -> int:
    return y0 * (y0 + 1) // 2


def part_2(x0: int, x1: int, y0: int, y1: int) -> int:
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


def parse_input():
    instruction = "target area: x=206..250, y=-105..-57"
    return [int(n) for n in re.findall(r"-?\d+", instruction)]


if __name__ == "__main__":
    x_min, x_max, y_min, y_max = parse_input()

    print(f"Part 1: The highest possible y-value on the probes trajectory is {part_1(y_min)}.")

    print(f"Part 2: There are {part_2(x_min, x_max, y_min, y_max)} different velocities from which you end up in the "
          f"target.")
