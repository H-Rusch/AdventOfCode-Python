
from .intcode import intcode


def part1(input):
    instructions = parse(input)

    computer = intcode.IntcodeV3_21(instructions)
    computer.execute_program()

    return computer.output[2::3].count(2)


def part2(input):
    instructions = parse(input)
    instructions[0] = 2

    computer = intcode.IntcodeV3_21(instructions)
    computer.execute_program()

    tiles = computer.output

    ball_x = tiles.index(4) - 2
    paddle_x = tiles.index(3) - 2
    score = 0

    while computer.running != 0:
        if ball_x > paddle_x:
            computer.input = 1
        elif ball_x < paddle_x:
            computer.input = -1
        else:
            computer.input = 0
        computer.execute_program()

        # render_game(generate_tile_map(computer.output))
        i = 0
        while i < len(tiles):

            if tiles[i + 2] == 4:
                ball_x = tiles[i]
            elif tiles[i + 2] == 3:
                paddle_x = tiles[i]
            elif tiles[i] == -1 and tiles[i + 1] == 0:
                score = tiles[i + 2]
            i += 3

    return score


def generate_tile_map(output: list) -> dict:
    tile_map = dict()

    i = 0
    while i < len(output):
        x = output[i]
        y = output[i + 1]
        tile = output[i + 2]

        tile_map[(x, y)] = tile

        i += 3

    return tile_map


def render_game(tiles: dict):
    x_values = list(map(lambda k: k[0], tiles.keys()))
    y_values = list(map(lambda k: k[1], tiles.keys()))
    min_x, max_x = min(x_values), max(x_values)
    min_y, max_y = min(y_values), max(y_values)

    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            tile = tiles.get((x, y))
            if tile == 0:
                line += "  "
            elif tile == 1:
                line += "□ "
            elif tile == 2:
                line += "# "
            elif tile == 3:
                line += "_ "
            elif tile == 4:
                line += "o "

        print(line)


def parse(input):
    return [int(n) for n in input.split(",")]
