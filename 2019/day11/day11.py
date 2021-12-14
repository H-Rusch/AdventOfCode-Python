class IntcodeV3_1:
    def __init__(self, program: list):
        self.memory = program[:]
        for _ in range(10000):
            self.memory.append(0)
        # running . 0: stopped, 1: running, 2: pausing
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
                user_input = self.input
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

        # print("Diagnostic output:", self.output)

        self.running = 2

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


def part_1(program: list):
    tiles_painted = paint(program)

    return len(tiles_painted.keys())


def part_2(program: list):
    tiles_painted = paint(program, start_on_white=True)

    print_hull(tiles_painted)


def print_hull(tiles_painted: dict):
    min_x = min(map(lambda t: t[0], tiles_painted.keys()))
    max_x = max(map(lambda t: t[0], tiles_painted.keys()))

    min_y = min(map(lambda t: t[1], tiles_painted.keys()))
    max_y = max(map(lambda t: t[1], tiles_painted.keys()))

    for y in reversed(range(min_y, max_y + 1)):
        print(" ".join(["█" if tiles_painted.get((x, y), 0) == 1 else " " for x in range(min_x, max_x + 1)]))


def paint(program: list, start_on_white: bool = False) -> dict:
    computer = IntcodeV3_1(program)

    tiles_painted = dict()
    # 0: n, 1: w, 2: s, 3: e
    direction = 0
    x, y = 0, 0

    if start_on_white:
        tiles_painted[(x, y)] = 1

    while computer.running in [1, 2]:
        # input the color the robot stands on
        computer.input = tiles_painted.get((x, y), 0)
        computer.execute_program()

        # robot outputs the color to paint with
        tiles_painted[(x, y)] = computer.output
        computer.execute_program()

        # turn the robot
        if computer.output == 0:
            direction = (direction + 1) % 4
        elif computer.output == 1:
            direction = (direction - 1) % 4
        else:
            raise Exception("Output is not a valid direction")

        # go one tile forwards
        if direction == 0:
            y += 1
        elif direction == 1:
            x -= 1
        elif direction == 2:
            y -= 1
        else:
            x += 1

    return tiles_painted


def parse_input():
    with open("input.txt", "r") as file:
        return [int(n) for n in file.read().split(",")]


if __name__ == "__main__":
    instructions = parse_input()

    print(f"Part 1: The robot paints {part_1(instructions)} tiles at least once.")

    print("Part 2: The robot paints the following on the hull:")
    part_2(instructions)
