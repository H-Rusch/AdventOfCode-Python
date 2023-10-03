class Device:
    def __init__(self, registers: list):
        self.registers = registers
        self.lookup = {0: self.eqir,
                       1: self.addi,
                       2: self.gtir,
                       3: self.setr,
                       4: self.mulr,
                       5: self.seti,
                       6: self.muli,
                       7: self.eqri,
                       8: self.bori,
                       9: self.bani,
                       10: self.gtrr,
                       11: self.eqrr,
                       12: self.addr,
                       13: self.gtri,
                       14: self.borr,
                       15: self.banr}

    def execute(self, opcode: int, A: int, B: int, C: int):
        self.lookup[opcode](A, B, C)

    def addr(self, A, B, C):
        self.registers[C] = self.registers[A] + self.registers[B]

    def addi(self, A, B, C):
        self.registers[C] = self.registers[A] + B

    def mulr(self, A, B, C):
        self.registers[C] = self.registers[A] * self.registers[B]

    def muli(self, A, B, C):
        self.registers[C] = self.registers[A] * B

    def banr(self, A, B, C):
        self.registers[C] = self.registers[A] & self.registers[B]

    def bani(self, A, B, C):
        self.registers[C] = self.registers[A] & B

    def borr(self, A, B, C):
        self.registers[C] = self.registers[A] | self.registers[B]

    def bori(self, A, B, C):
        self.registers[C] = self.registers[A] | B

    def setr(self, A, B, C):
        self.registers[C] = self.registers[A]

    def seti(self, A, B, C):
        self.registers[C] = A

    def gtir(self, A, B, C):
        self.registers[C] = 1 if A > self.registers[B] else 0

    def gtri(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] > B else 0

    def gtrr(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] > self.registers[B] else 0

    def eqir(self, A, B, C):
        self.registers[C] = 1 if A == self.registers[B] else 0

    def eqri(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] == B else 0

    def eqrr(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] == self.registers[B] else 0


def part1(input: str) -> int:
    samples, _ = parse(input)

    sample_count = 0

    for sample in samples.split("\n\n"):
        before, instruction, after = sample.splitlines()
        before = extract_num_list(before)
        instruction = extract_params(instruction)
        after = extract_num_list(after)

        count = 0
        for opcode in range(16):
            device = Device(before[:])
            device.execute(opcode, instruction[1], instruction[2], instruction[3])
            if device.registers == after:
                count += 1
        if count >= 3:
            sample_count += 1

    return sample_count



def part2(input: str) -> int:
    _, instructions = parse(input)

    device = Device([0, 0, 0, 0])
    for instruction in instructions.splitlines():
        device.execute(*extract_params(instruction))

    return device.registers[0]


def extract_num_list(list_repr: str) -> list:
    to_remove = "[],"
    for letter in to_remove:
        list_repr = list_repr.replace(letter, "")

    return [int(s) for s in list_repr[7:].split()]


def extract_params(instruction_str: str) -> list:
    return [int(s) for s in instruction_str.split()]



def helper(samples: str):
    # helper function to find which opcode is which instruction.
    # expects the lookup directory in the Device-class to assign the n
    # umbers 0 to 15 to the operations in the same order they are defined in the text
    to_assign = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    for sample in samples.split("\n\n"):
        before, instruction, after = sample.splitlines()
        before = extract_num_list(before)
        instruction = extract_params(instruction)
        after = extract_num_list(after)

        count = 0
        for opcode in to_assign:
            device = Device(before[:])
            device.execute(opcode, instruction[1], instruction[2], instruction[3])
            if device.registers == after:
                count += 1

        if count == 1:
            for opcode in to_assign:
                device = Device(before[:])
                device.execute(opcode, instruction[1], instruction[2], instruction[3])

                if device.registers == after:
                    print(f"{opcode} means the {opcode}st/nd/rd/th generated operation")
                    to_assign.remove(opcode)
                    break


def parse(input):
    return input.split("\n\n\n\n")
