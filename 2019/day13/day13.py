class IntcodeV3_2:
    def __init__(self, program: list):
        self.memory = program[:]
        for _ in range(10000):
            self.memory.append(0)
        self.running = 1
        self.pc = 0
        self.relative_base = 0

        self.output = []
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
        self.output.append(parameters[0])
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


def part_1(instructions: list):
    computer = IntcodeV3_2(instructions)
    computer.execute_program()

    return computer.output[2::3].count(2)


def part_2(instructions: list):
    computer = IntcodeV3_2(instructions)
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


def parse_input():
    with open("input.txt", "r") as file:
        return [int(n) for n in file.read().split(",")]


if __name__ == "__main__":
    numbers = parse_input()
    numbers2 = numbers[:]
    numbers2[0] = 2

    print(f"After the game ended, there are {part_1(numbers)} block tiles left.")

    print(f"The score after the last block is broken is {part_2(numbers2)}.")
