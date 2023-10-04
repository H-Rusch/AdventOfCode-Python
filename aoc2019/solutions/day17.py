from .intcode import intcode


def part1(input):
    instructions = parse(input)
    tiles = generate_tile_map(instructions)
    # print_scaffold(tiles)
    intersections = find_intersections(tiles)

    return sum(map(lambda c: c[0] * c[1], intersections))


def part2(input):
    instructions = parse(input)
    tiles = generate_tile_map(instructions)
    # print_scaffold(tiles)
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
    computer = intcode.IntcodeV3_3(instructions)
    movement = "A,B,B,A,C,B,C,C,B,A\nR,10,R,8,L,10,L,10\nR,8,L,6,L,6\nL,10,R,10,L,6\nn\n"
    i = 0

    # computer.execute_program()
    while i < len(movement):
        computer.input = ord(movement[i])
        i += 1
        computer.execute_program()
        while computer.running == 3:
            computer.execute_program()

    while computer.running != 0:
        computer.execute_program()

    return computer.output


def find_path(tiles: dict) -> list:
    x, y = 0, 0
    # 0: up, 1: down, 2: left, 3: right
    direction = 0
    for (dx, dy), tile in tiles.items():
        if tile in ["^", "v", "<", ">"]:
            x, y = dx, dy
            direction = ["^", "v", "<", ">"].index(tile)
            break

    instructions = []
    steps = 0
    while True:
        # try to go forward
        dx, dy = get_forward(x, y, direction)
        if tiles.get((dx, dy), ".") == "#":
            steps += 1
            x, y = dx, dy
        else:
            instructions.append(str(steps))
            # if forward is empty, try right and if that fails try left
            if tiles.get(get_right(x, y, direction), ".") == "#":
                steps = 0
                instructions.append("R")
                direction = clockwise(direction)
            elif tiles.get(get_left(x, y, direction), ".") == "#":
                steps = 0
                instructions.append("L")
                direction = counter_clockwise(direction)
            else:
                break

    return instructions


def get_forward(x: int, y: int, direction: int) -> tuple[int, int]:
    if direction == 0:
        return x, y - 1
    elif direction == 1:
        return x, y + 1
    elif direction == 2:
        return x - 1, y
    elif direction == 3:
        return x + 1, y


def get_right(x: int, y: int, direction: int) -> tuple[int, int]:
    if direction == 0:
        return x + 1, y
    elif direction == 1:
        return x - 1, y
    elif direction == 2:
        return x, y - 1
    elif direction == 3:
        return x, y + 1


def get_left(x: int, y: int, direction: int) -> tuple[int, int]:
    if direction == 0:
        return x - 1, y
    elif direction == 1:
        return x + 1, y
    elif direction == 2:
        return x, y + 1
    elif direction == 3:
        return x, y - 1


def clockwise(d: int) -> int:
    if d == 0:
        return 3
    if d == 1:
        return 2
    if d == 2:
        return 0
    if d == 3:
        return 1


def counter_clockwise(d: int) -> int:
    if d == 0:
        return 2
    if d == 1:
        return 3
    if d == 2:
        return 1
    if d == 3:
        return 0


def get_adjacent(x: int, y: int) -> list:
    return [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]


def generate_tile_map(instructions: list) -> dict:
    computer = intcode.IntcodeV3_3(instructions)
    x, y = 0, 0

    coordinates = dict()

    while computer.running != 0:
        computer.execute_program()

        code = computer.output

        # 95: ^, 118: v, 60: <, 62: >
        if code in [35, 46, 94, 118, 60, 62]:
            coordinates[(x, y)] = chr(code)
            x += 1
        elif code == 10:
            x = 0
            y += 1
        else:
            print(code)

    return coordinates


def find_intersections(tiles: dict):
    intersections = []
    scaffold_symbols = ["#", "^", "v", "<", ">"]
    for (x, y), tile in tiles.items():
        if tile in scaffold_symbols:
            if all([tiles.get((dx, dy), "") in scaffold_symbols for (dx, dy) in get_adjacent(x, y)]):
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
