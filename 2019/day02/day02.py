class Intcode:
    def __init__(self, program: list):
        self.memory = program[:]

    def execute_program(self):
        pc = 0
        while True:
            opcode = self.memory[pc]
            if opcode == 99:
                break
            elif opcode == 1:
                self.add(self.memory[pc + 1], self.memory[pc + 2], self.memory[pc + 3])
            elif opcode == 2:
                self.mult(self.memory[pc + 1], self.memory[pc + 2], self.memory[pc + 3])
            else:
                raise Exception("Instruction unknown")

            pc += 4

    def add(self, adr1: int, adr2: int, destination: int):
        self.memory[destination] = self.memory[adr1] + self.memory[adr2]

    def mult(self, adr1: int, adr2: int, destination: int):
        self.memory[destination] = self.memory[adr1] * self.memory[adr2]


def part_1(program: list) -> int:
    program[1] = 12
    program[2] = 2
    computer = Intcode(program)
    computer.execute_program()

    return computer.memory[0]


def part_2(program: list) -> int:
    for noun in range(100):
        for verb in range(100):
            program[1] = noun
            program[2] = verb

            computer = Intcode(program)
            computer.execute_program()

            if computer.memory[0] == 19690720:
                return 100 * noun + verb

    return -1


def parse_input():
    with open("input.txt", "r") as file:
        return [int(s) for s in file.read().split(",")]


if __name__ == "__main__":
    instruction_list = parse_input()

    print(f"Part 1: The number at address 0 after executing the program is {part_1(instruction_list)}.")

    print(f"Part 2: 100 * noun + verb which produce the desired output is {part_2(instruction_list)}.")
