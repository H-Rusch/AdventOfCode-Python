# resource for hexagon coordinates: https://www.redblobgames.com/grids/hexagons/

ORIGIN = (0, 0)


def part1(input):
    coordinate = ORIGIN
    for step in input.split(","):
        coordinate = take_step(*coordinate, step)

    return hex_distance(coordinate, ORIGIN)


def part2(input):
    coordinate = ORIGIN
    max_distance = 0
    for step in input.split(","):
        coordinate = take_step(*coordinate, step)
        max_distance = max(max_distance, hex_distance(coordinate, ORIGIN))

    return max_distance


def take_step(x: int, y: int, step: str) -> (int, int):
    match step:
        case "n":
            return (x, y - 2)
        case "ne":
            return (x + 1, y - 1)
        case "nw":
            return (x - 1, y - 1)
        case "s":
            return (x, y + 2)
        case "se":
            return (x + 1, y + 1)
        case "sw":
            return (x - 1, y + 1)
        case _:
            raise ValueError("Step not supported:", step)


def hex_distance(a: (int, int), b: (int, int)) -> int:
    dcol = abs(a[0] - b[0])
    drow = abs(a[1] - b[1])

    return dcol + max(0, (drow - dcol) // 2)
