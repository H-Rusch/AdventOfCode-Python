import math


class Device:
    def __init__(self, registers: list, bound: int, instructions: list):
        self.registers = registers
        self.ip = 0
        self.bound = bound
        self.lookup = {
            "eqir": self.eqir,
            "addi": self.addi,
            "gtir": self.gtir,
            "setr": self.setr,
            "mulr": self.mulr,
            "seti": self.seti,
            "muli": self.muli,
            "eqri": self.eqri,
            "bori": self.bori,
            "bani": self.bani,
            "gtrr": self.gtrr,
            "eqrr": self.eqrr,
            "addr": self.addr,
            "gtri": self.gtri,
            "borr": self.borr,
            "banr": self.banr,
        }
        self.instructions = instructions

    def run(self):
        while 0 <= self.ip < len(self.instructions):
            self.execute(*self.instructions[self.ip])

    def execute(self, opcode: str, A: int, B: int, C: int):
        self.registers[self.bound] = self.ip
        self.lookup[opcode](A, B, C)
        self.ip = self.registers[self.bound]
        self.ip += 1

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
    bound_register, instructions = parse(input)

    computer = Device([0, 0, 0, 0, 0, 0], bound_register, instructions)
    computer.run()

    return computer.registers[0]


def part2(_) -> int:
    """Program decoded from the input (see input_decoded.txt). Initial steps for reverse engineering came from
    https://www.reddit.com/r/adventofcode/comments/a7j9zc/2018_day_19_solutions/ec3v5ud/ by /u/Stan-It."""

    r5 = 10_550_400 + 967
    r0 = r5 + 1

    root = int(math.sqrt(r5))
    for r4 in range(2, root + 1):
        if r5 % r4 == 0:
            r0 += r4 + r5 // r4

    return r0


def parse(input):
    instructions = input.strip().splitlines()
    bound = int(instructions[0][4])
    processed_instructions = []
    for instruction in instructions[1:]:
        opcode, a, b, c = instruction.split()
        processed_instructions.append([opcode, int(a), int(b), int(c)])

    return bound, processed_instructions
