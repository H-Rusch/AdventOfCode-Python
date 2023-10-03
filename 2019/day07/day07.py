from itertools import permutations
from collections import deque


class IntcodeV2_5:
    def __init__(self, program: list, phase_setting):
        self.memory = program[:]
        # halt: 0 = running, 1 = paused, 2 = execution finished
        self.halt = 0
        self.pc = 0

        self.phase_setting = phase_setting
        self.phase_setting_needed = True
        self.input_value = None
        self.output_value = None

    def execute_program(self):
        self.halt = 0
        while self.halt == 0:
            opcode = str(self.memory[self.pc])
            self.parse_opcode(opcode.zfill(5))

    def parse_opcode(self, opcode: str):
        op = int(opcode[-2:])
        if op == 99:
            self.halt = 2

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
                # the first time the input is made, the phase setting is set
                # after that, the value fed into the amplifier is set
                user_input = self.phase_setting if self.phase_setting_needed else self.input_value
                self.phase_setting_needed = False

                self.save_value(user_input, parameter)

            else:
                self.diagnostic_output(parameter, parameter_mode)

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

    def diagnostic_output(self, value: int, parameter_mode: str):
        output = value if parameter_mode == "1" else self.memory[value]

        # after putting out a value wait with further execution until a new input value is set
        self.output_value = output
        self.halt = 1

        # print("Diagnostic output:", output)

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


def part1(program: list):
    maximum_value = 0

    for p1, p2, p3, p4, p5 in permutations(range(5)):
        amplifier_a = IntcodeV2_5(program, p1)
        amplifier_a.input_value = 0
        amplifier_a.execute_program()

        amplifier_b = IntcodeV2_5(program, p2)
        amplifier_b.input_value = amplifier_a.output_value
        amplifier_b.execute_program()

        amplifier_c = IntcodeV2_5(program, p3)
        amplifier_c.input_value = amplifier_b.output_value
        amplifier_c.execute_program()

        amplifier_d = IntcodeV2_5(program, p4)
        amplifier_d.input_value = amplifier_c.output_value
        amplifier_d.execute_program()

        amplifier_e = IntcodeV2_5(program, p5)
        amplifier_e.input_value = amplifier_d.output_value
        amplifier_e.execute_program()

        if amplifier_e.output_value > maximum_value:
            maximum_value = amplifier_e.output_value

    return maximum_value


def part2(program: list):
    maximum_value = 0

    for p1, p2, p3, p4, p5 in permutations(range(5, 10)):
        amplifiers = deque()
        amplifiers.append(IntcodeV2_5(program, p1))
        amplifiers.append(IntcodeV2_5(program, p2))
        amplifiers.append(IntcodeV2_5(program, p3))
        amplifiers.append(IntcodeV2_5(program, p4))
        amplifiers.append(IntcodeV2_5(program, p5))

        input_to_next = 0

        # Until the queue of amplifiers is empty, which happens when amplifier E halts, calculate the output for the
        # amplifiers. The output is fed as input into the next amplifier. Feeding the output pauses an amplifier
        while len(amplifiers) > 0:
            amplifier = amplifiers.popleft()

            amplifier.input_value = input_to_next

            amplifier.execute_program()

            input_to_next = amplifier.output_value

            if amplifier.halt != 2:
                amplifiers.append(amplifier)
            elif input_to_next > maximum_value:
                maximum_value = input_to_next

    return maximum_value


def parse(input):
    with open("input.txt", "r") as file:
        return [int(n) for n in file.read().split(",")]


if __name__ == "__main__":
    instructions = parse(input)

    print(f"Part 1: The highest signal that can be sent to the thrusters is {part1(instructions)}.")

    print(f"Part 2: The highest signal that can be sent to the thrusters when the amplifiers are installed with a "
          f"feedback loop is {part2(instructions)}.")
