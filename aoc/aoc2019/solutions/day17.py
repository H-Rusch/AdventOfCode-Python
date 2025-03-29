from collections import deque
from aoc.aoc2019.intcode.intcode import Intcode
from aoc.util.direction import Direction


def part1(input):
    instructions = parse(input)
    tiles = generate_tile_map(instructions)
    intersections = find_intersections(tiles)

    return sum(map(lambda c: c[0] * c[1], intersections))


def part2(input):
    instructions = parse(input)
    tiles = generate_tile_map(instructions)
    movement = find_path(tiles)[1:]
    """
    manually compressing the instruction list:
    R, 10, R, 8, L, 10, L, 10, R, 8, L, 6, L, 6, R, 8, L, 6, L, 6, R, 10, R, 8, L, 10, L, 10, L, 10, R, 10, L, 6, R, 8, L, 6, L, 6, L, 10, R, 10, L, 6, L, 10, R, 10, L, 6, R, 8, L, 6, L, 6, R, 10, R, 8, L, 10, L, 10
    =>
    A, B, B, A, C, B, C, C, B, A
        
    A: R, 10, R, 8, L, 10, L, 10 
    B: R, 8, L, 6, L, 6
    C: L, 10, R, 10, L, 6
    """
    instructions[0] = 2
    computer = Intcode(instructions)
    movement = (
        "A,B,B,A,C,B,C,C,B,A\nR,10,R,8,L,10,L,10\nR,8,L,6,L,6\nL,10,R,10,L,6\nn\n"
    )

    computer.inputs = deque([ord(ch) for ch in movement])
    computer.run()

    return computer.get_latest_output()


def generate_tile_map(instructions: list) -> dict:
    computer = Intcode(instructions)
    computer.run()

    x, y = 0, 0
    coordinates = dict()
    for tile in [chr(code) for code in computer.outputs]:
        if tile in ["^", "v", "<", ">", "#", "."]:
            coordinates[(x, y)] = tile
            x += 1
        elif tile == "\n":
            x = 0
            y += 1

    return coordinates


def find_path(tiles: dict) -> list:
    position = (0, 0)
    direction = Direction.UP
    for (dx, dy), tile in tiles.items():
        if tile in ["^", "v", "<", ">"]:
            position = dx, dy
            direction = Direction.from_str(tile)
            break

    instructions = []
    steps = 0
    while True:
        # try to go forward
        if tiles.get(forward := direction.steps(position), ".") == "#":
            steps += 1
            position = forward
        else:
            instructions.append(str(steps))
            # if forward is empty, try right and if that fails try left
            if tiles.get(get_right(position, direction), ".") == "#":
                steps = 0
                instructions.append("R")
                direction = direction.turn_right()
            elif tiles.get(get_left(position, direction), ".") == "#":
                steps = 0
                instructions.append("L")
                direction = direction.turn_left()
            else:
                break

    return instructions


def get_right(position: tuple[int, int], direction: Direction) -> tuple[int, int]:
    return direction.turn_right().steps(position)


def get_left(position: tuple[int, int], direction: Direction) -> tuple[int, int]:
    return direction.turn_right().steps(position)


def get_adjacent(x: int, y: int) -> list:
    return [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]


def find_intersections(tiles: dict):
    intersections = []
    scaffold_symbols = ["#", "^", "v", "<", ">"]
    for (x, y), tile in tiles.items():
        if tile in scaffold_symbols:
            if all(
                [
                    tiles.get((dx, dy), "") in scaffold_symbols
                    for (dx, dy) in get_adjacent(x, y)
                ]
            ):
                intersections.append((x, y))

    return intersections


def print_scaffold(tiles: dict):
    x_values = list(map(lambda c: c[0], tiles.keys()))
    y_values = list(map(lambda c: c[1], tiles.keys()))

    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)

    for y in range(y_min, y_max + 1):
        line = ""
        for x in range(x_min, x_max + 1):
            tile = tiles.get((x, y), " ")
            line += tile + " "

        print(line)


def parse(input):
    return [int(n) for n in input.split(",")]
