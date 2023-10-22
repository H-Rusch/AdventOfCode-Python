from collections import defaultdict


class CPU:
    def __init__(self, instructions: list) -> None:
        self.instructions = instructions
        self.registers = defaultdict(int)
        self.ic = 0
        self.mul_count = 0

    def execute_program(self):
        while self.ic in range(len(self.instructions)):
            instruction = self.instructions[self.ic]
            self.ic += self.execute_instruction(*instruction)

    def execute_instruction(self, operation: str, arg1: str, arg2: str = None) -> int:
        match operation:
            case "set":
                self.registers[arg1] = self.get_value(arg2)
            case "sub":
                self.registers[arg1] -= self.get_value(arg2)
            case "mul":
                self.registers[arg1] *= self.get_value(arg2)
                self.mul_count += 1
            case "jnz":
                if self.get_value(arg1) != 0:
                    return self.get_value(arg2)
            case _:
                raise ValueError(f"Operation not supported: {operation}")

        return 1

    def get_value(self, value: str) -> int:
        if value.lstrip("-").isnumeric():
            return int(value)
        return self.registers[value]


def part1(input):
    instructions = parse(input)

    card = CPU(instructions)
    card.execute_program()

    return card.mul_count


def part2(input):
    """I did not deconstruct the assembly code myself. I found out from the subreddit what the program is doing and implemented that. """
    h = 0

    b = c = int(input.split()[2])

    start_b = b * 100 + 100000
    c = start_b + 17000

    for b in range(start_b, c + 1, 17):
        if not is_prime(b):
            h += 1

    return h


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5), 2):
        if n % i == 0:
            return False
    return True


def parse(input: str) -> list[list[str]]:
    return [line.split() for line in input.splitlines()]
