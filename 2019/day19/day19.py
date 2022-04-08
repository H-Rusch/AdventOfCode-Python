class IntcodeV3_3:
    def __init__(self, program: list):
        self.memory = program[:]
        for _ in range(100):
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


# --- code for day 19 -------------------------------------
def part_1(instructions: list) -> int:
    def horizontal(start_x, start_y):
        count = 0
        x = start_x
        start_found = False
        while x < 50:
            if test_coordinate(instructions, x, start_y):
                count += 1
                start_found = True
            elif start_found:  # stop searching after the beam
                break
            x += 1

        return count

    affected = 0
    for y in range(50):
        affected += horizontal(0, y)

    return affected


def part_2(instructions: list) -> int:
    def find_first(last_x: int, dy: int) -> int:
        dx = int(last_x * 0.9)
        while True:
            if test_coordinate(instructions, dx, dy):
                return dx
            dx += 1

    def test_square(x: int, y: int):
        """Top left not tested, because it is tested before this call. """
        if test_coordinate(instructions, x, y + size) and test_coordinate(instructions, x + size, y) and \
                test_coordinate(instructions, x + size, y + size):
            return True, (x, y)
        return False, (0, 0)

    size = 99
    x, y = 0, 10
    while True:
        x = find_first(x, y)

        while test_coordinate(instructions, x, y):
            b, (dx, dy) = test_square(x, y)
            if b:
                return dx * 10000 + dy
            x += 1
        y += 1


def test_coordinate(instructions: list, x: int, y: int) -> bool:
    computer = IntcodeV3_3(instructions)
    computer.input = x
    computer.execute_program()
    computer.input = y
    computer.execute_program()

    return computer.output == 1


def parse_input():
    with open("input.txt", "r") as file:
        return [int(n) for n in file.read().split(",")]


if __name__ == "__main__":
    numbers = parse_input()

    print(f"Part 1: {part_1(numbers)} points are affected by the tractor beam.")

    print(f"Part 2: The calculated score for the closest emitter is {part_2(numbers)}.")
