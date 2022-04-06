class IntcodeV3_2:
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
    """ Generate the tile map and then go through it breadth-first until the goal is reached. """
    tiles = generate_tile_map(instructions)
    x, y = 0, 0
    expanded = [(x, y, 0)]
    visited = set()

    while True:
        expanded.sort(key=lambda c: c[2])
        x, y, cost = expanded.pop(0)
        visited.add((x, y))

        for (ad_x, ad_y) in get_adjacent(x, y):
            if (ad_x, ad_y) not in visited and tiles.get((ad_x, ad_y), 0) != 0:
                expanded.append((ad_x, ad_y, cost + 1))

        if tiles.get((x, y)) == 2:
            return cost


def part_2(instructions: list):
    """ Pretty much the same algorithm from part 1,
    except now we start at the 'end' and we stop when all tiles have been visited.
    """
    tiles = generate_tile_map(instructions)
    x, y = 0, 0
    for (k_x, k_y), status in tiles.items():
        if status == 2:
            x, y = k_x, k_y
            break

    expanded = [(x, y, 0)]
    visited = set()

    while True:
        expanded.sort(key=lambda c: c[2])
        x, y, time = expanded.pop(0)
        visited.add((x, y))
        tiles[(x, y)] = 4

        for (ad_x, ad_y) in get_adjacent(x, y):
            if (ad_x, ad_y) not in visited and tiles.get((ad_x, ad_y), 0) != 0:
                expanded.append((ad_x, ad_y, time + 1))

        if len(expanded) == 0:
            return time


def get_adjacent(x: int, y: int) -> list:
    return [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]


def generate_tile_map(instructions: list) -> dict:
    """
    Stick to the right wall by following basic rules.
    If the robot moves onto an empty field, it turns right and tries to move forward.
    If the robot walked against a wall, it turns left and tries to move forward.
    """

    def clockwise(d):
        if d == 1:
            return 4
        if d == 2:
            return 3
        if d == 3:
            return 1
        if d == 4:
            return 2

    def counter_clockwise(d):
        if d == 1:
            return 3
        if d == 2:
            return 4
        if d == 3:
            return 2
        if d == 4:
            return 1

    computer = IntcodeV3_2(instructions)
    direction = 1
    x, y = 0, 0

    coordinates = dict()
    to_check, checked = set(), set()

    while computer.running != 0:
        computer.input = direction
        computer.execute_program()

        status = computer.output

        if (x, y) not in checked:
            for d in [1, 2, 3, 4]:
                to_check.add((x, y, d))

        # calculate the coordinate of the tile which is examined
        examining_x, examining_y = x, y
        if direction == 1:
            examining_y -= 1
        elif direction == 2:
            examining_y += 1
        elif direction == 3:
            examining_x -= 1
        elif direction == 4:
            examining_x += 1

        coordinates[(examining_x, examining_y)] = status

        # turn left when hitting a wall, turn right otherwise
        if status == 0:
            direction = counter_clockwise(direction)
        else:
            direction = clockwise(direction)
            x, y = examining_x, examining_y

        to_check.discard((x, y, direction))
        checked.add((x, y))

        if len(to_check) == 0:
            break

    return coordinates


def print_maze(tiles: dict):
    x_values = list(map(lambda c: c[0], tiles.keys()))
    y_values = list(map(lambda c: c[1], tiles.keys()))

    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)

    for y in range(y_min, y_max + 1):
        line = ""
        for x in range(x_min, x_max + 1):
            status = tiles.get((x, y), 3)
            if (x, y) == (0, 0):
                line += "S "
            elif status == 0:
                line += "□ "
            elif status == 1:
                line += "  "
            elif status == 2:
                line += "x "
            elif status == 3:
                line += "? "
            elif status == 4:
                line += "O "

        print(line)


def parse_input():
    with open("input.txt", "r") as file:
        return [int(n) for n in file.read().split(",")]


if __name__ == "__main__":
    numbers = parse_input()

    print(f"Part 1: The fewest number of moves to get to the oxygen system is {part_1(numbers)}.")

    print(f"Part 2: After {part_2(numbers)} minutes the area is flooded with oxygen.")
