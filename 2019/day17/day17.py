class IntcodeV3_3:
    def __init__(self, program: list):
        self.memory = program[:]
        for _ in range(10000):
            self.memory.append(0)
        self.running = 1
        self.pc = 0
        self.relative_base = 0

        self.output = None
        self.input = None

    def execute_program(self):
        self.running = 1
        while self.running == 1:
            opcode = str(self.memory[self.pc])

            self.parse_opcode(opcode.zfill(5))

    # Decoding instructions --------------
    def parse_opcode(self, opcode: str):
        op = int(opcode[-2:])
        parameter_modes = list(reversed(opcode[:3]))
        if op == 99:
            self.running = 0

        # add and mult
        elif op in [1, 2]:
            parameters = [self.parse_parameter_freely(parameter_modes[0], self.memory[self.pc + 1]),
                          self.parse_parameter_freely(parameter_modes[1], self.memory[self.pc + 2]),
                          self.parse_parameter_restricted(parameter_modes[2], self.memory[self.pc + 3])]

            if op == 1:
                self.add(parameters)

            elif op == 2:
                self.mult(parameters)

            self.pc += 4

        # input and output
        elif op in [3, 4]:
            if op == 3:
                if self.input is not None:
                    user_input = self.input
                    self.input = None
                else:
                    self.running = 2
                    return
                # user_input = int(input("Which value to save?: "))
                parameters = [user_input,
                              self.parse_parameter_restricted(parameter_modes[0], self.memory[self.pc + 1])]

                self.write_value(parameters)

            else:
                parameters = [self.parse_parameter_freely(parameter_modes[0], self.memory[self.pc + 1])]

                self.output_value(parameters)

            self.pc += 2

        # jumps
        elif op in [5, 6]:
            parameters = [self.parse_parameter_freely(parameter_modes[0], self.memory[self.pc + 1]),
                          self.parse_parameter_freely(parameter_modes[1], self.memory[self.pc + 2])]

            if op == 5:
                self.jump_if_true(parameters)

            else:
                self.jump_if_false(parameters)

        # comparisons
        elif op in [7, 8]:
            parameters = [self.parse_parameter_freely(parameter_modes[0], self.memory[self.pc + 1]),
                          self.parse_parameter_freely(parameter_modes[1], self.memory[self.pc + 2]),
                          self.parse_parameter_restricted(parameter_modes[2], self.memory[self.pc + 3])]

            if op == 7:
                self.less_than(parameters)

            else:
                self.equals(parameters)

            self.pc += 4

        # adjust relative base
        elif op == 9:
            parameters = [self.parse_parameter_freely(parameter_modes[0], self.memory[self.pc + 1])]

            self.adjust_relative_base(parameters)

            self.pc += 2

        else:
            raise Exception("Instruction unknown:", opcode)

    # concrete implementation of functionality ----------------
    def parse_parameter_freely(self, parameter_mode: str, value: int) -> int:
        if parameter_mode == "0":
            return self.memory[value]

        elif parameter_mode == "1":
            return value

        elif parameter_mode == "2":
            return self.memory[value + self.relative_base]

        else:
            raise Exception("Parameter Mode unknown")

    def parse_parameter_restricted(self, parameter_mode: str, value: int) -> int:
        """ To be used when an address value should be given for a parameter. """
        if parameter_mode in ["0", "1"]:
            return value

        elif parameter_mode == "2":
            return value + self.relative_base

        else:
            raise Exception("Parameter Mode unknown")

    def add(self, parameters: list):
        value1 = parameters[0]
        value2 = parameters[1]
        destination = parameters[2]

        self.memory[destination] = value1 + value2

    def mult(self, parameters: list):
        value1 = parameters[0]
        value2 = parameters[1]
        destination = parameters[2]

        self.memory[destination] = value1 * value2

    def write_value(self, parameters: list):
        value = parameters[0]
        adr = parameters[1]

        self.memory[adr] = value

    def output_value(self, parameters: list):
        self.output = parameters[0]
        self.running = 3
        # print("Diagnostic output:", self.output[-1])

    def jump_if_true(self, parameters: list):
        param1 = parameters[0]
        param2 = parameters[1]

        if param1 != 0:
            self.pc = param2
        else:
            self.pc += 3

    def jump_if_false(self, parameters: list):
        param1 = parameters[0]
        param2 = parameters[1]

        if param1 == 0:
            self.pc = param2
        else:
            self.pc += 3

    def less_than(self, parameters: list):
        param1 = parameters[0]
        param2 = parameters[1]
        adr = parameters[2]

        if param1 < param2:
            self.memory[adr] = 1
        else:
            self.memory[adr] = 0

    def equals(self, parameters: list):
        param1 = parameters[0]
        param2 = parameters[1]
        adr = parameters[2]

        if param1 == param2:
            self.memory[adr] = 1
        else:
            self.memory[adr] = 0

    def adjust_relative_base(self, parameters: list):
        value = parameters[0]

        self.relative_base += value


# --- actual functionality ----------------------------------------------
def part_1(instructions: list):
    tiles = generate_tile_map(instructions)
    # print_scaffold(tiles)
    intersections = find_intersections(tiles)

    return sum(map(lambda c: c[0] * c[1], intersections))


def part_2(instructions: list):
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
    computer = IntcodeV3_3(instructions)
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
    computer = IntcodeV3_3(instructions)
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


def parse_input():
    with open("input.txt", "r") as file:
        return [int(n) for n in file.read().split(",")]


if __name__ == "__main__":
    numbers = parse_input()

    print(f"Part 1: The sum of all alignment parameters is {part_1(numbers)}.")

    print(f"Part 2: The vacuum has {part_2(numbers)} dust-units collected.")
