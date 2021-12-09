class Intcode_v2:
    def __init__(self, program: list):
        self.memory = program[:]
        self.running = True
        self.pc = 0

    def execute_program(self):
        while self.running:
            opcode = str(self.memory[self.pc])
            self.parse_opcode(opcode.zfill(5))

    def parse_opcode(self, opcode: str):
        op = int(opcode[-2:])
        if op == 99:
            self.running = False

        # add and mult
        elif op in [1, 2]:
            parameter_modes = [opcode[i] for i in [-3, -4, -5]]
            parameters = [self.memory[self.pc + i] for i in [1, 2, 3]]

            if op == 1:
                self.add(parameters, parameter_modes)

            elif op == 2:
                self.mult(parameters, parameter_modes)

            self.pc += 4

        # input and output
        elif op in [3, 4]:
            parameter_mode = opcode[-3]
            parameter = self.memory[self.pc + 1]

            if op == 3:
                user_input = int(input("Which value to save?: "))
                self.save_value(user_input, parameter)

            else:
                self.output_value(parameter, parameter_mode)

            self.pc += 2

        # jumps
        elif op in [5, 6]:
            parameter_modes = [opcode[i] for i in [-3, -4]]
            parameters = [self.memory[self.pc + i] for i in [1, 2]]

            if op == 5:
                self.jump_if_true(parameters, parameter_modes)

            else:
                self.jump_if_false(parameters, parameter_modes)

        # comparisons
        elif op in [7, 8]:
            parameter_modes = [opcode[i] for i in [-3, -4, -5]]
            parameters = [self.memory[self.pc + i] for i in [1, 2, 3]]

            if op == 7:
                self.less_than(parameters, parameter_modes)

            else:
                self.equals(parameters, parameter_modes)

            self.pc += 4

        else:
            raise Exception("Instruction unknown:", opcode)

    def add(self, parameters: list, parameter_modes: list):
        value1 = parameters[0] if parameter_modes[0] == "1" else self.memory[parameters[0]]
        value2 = parameters[1] if parameter_modes[1] == "1" else self.memory[parameters[1]]
        destination = parameters[2]

        self.memory[destination] = value1 + value2

    def mult(self, parameters: list, parameter_modes: list):
        value1 = parameters[0] if parameter_modes[0] == "1" else self.memory[parameters[0]]
        value2 = parameters[1] if parameter_modes[1] == "1" else self.memory[parameters[1]]
        destination = parameters[2]

        self.memory[destination] = value1 * value2

    def save_value(self, value: int, adr: int):
        self.memory[adr] = value

    def output_value(self, value: int, parameter_mode: str):
        output = value if parameter_mode == "1" else self.memory[value]
        print("Diagnostic output:", output)

    def jump_if_true(self, parameters: list, parameter_modes: list):
        param1 = parameters[0] if parameter_modes[0] == "1" else self.memory[parameters[0]]
        param2 = parameters[1] if parameter_modes[1] == "1" else self.memory[parameters[1]]
        if param1 != 0:
            self.pc = param2
        else:
            self.pc += 3

    def jump_if_false(self, parameters: list, parameter_modes: list):
        param1 = parameters[0] if parameter_modes[0] == "1" else self.memory[parameters[0]]
        param2 = parameters[1] if parameter_modes[1] == "1" else self.memory[parameters[1]]
        if param1 == 0:
            self.pc = param2
        else:
            self.pc += 3

    def less_than(self, parameters: list, parameter_modes: list):
        param1 = parameters[0] if parameter_modes[0] == "1" else self.memory[parameters[0]]
        param2 = parameters[1] if parameter_modes[1] == "1" else self.memory[parameters[1]]
        dest = parameters[2]

        if param1 < param2:
            self.memory[dest] = 1
        else:
            self.memory[dest] = 0

    def equals(self, parameters: list, parameter_modes: list):
        param1 = parameters[0] if parameter_modes[0] == "1" else self.memory[parameters[0]]
        param2 = parameters[1] if parameter_modes[1] == "1" else self.memory[parameters[1]]
        dest = parameters[2]

        if param1 == param2:
            self.memory[dest] = 1
        else:
            self.memory[dest] = 0


def part_1(program: list):
    computer = Intcode_v2(program)
    computer.execute_program()


def part_2(program: list):
    computer = Intcode_v2(program)
    computer.execute_program()


def parse_input():
    with open("input.txt", "r") as file:
        return [int(n) for n in file.read().split(",")]


if __name__ == "__main__":
    instructions = parse_input()

    print(f"Part 1: The diagnostic code is the last output before halting. Give initial input of '1':")
    part_1(instructions)

    print(f"Part 2: The diagnostic code is the last output before halting. Give initial input of '5':")
    part_2(instructions)
