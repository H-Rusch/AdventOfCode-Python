from dataclasses import dataclass
from collections import defaultdict
import re


INSTRUCTION_PATTERN = re.compile(r"(.*?) (dec|inc) (-?\d+) if (.*?) (.*)")


@dataclass
class Instruction:
    register: str
    # value handles both increasing and decreating values
    value: int
    condition_register: str
    condition: str


def part1(input):
    instructions = parse(input)
    registers, _ = perform_instructions(instructions)

    return highest_register_value(registers)


def part2(input):
    instructions = parse(input)
    _, max_value = perform_instructions(instructions)

    return max_value


def perform_instructions(instructions: list) -> dict[str, int]:
    registers = defaultdict(int)
    max_value = 0

    for instruction in instructions:
        if eval("registers[instruction.condition_register] " + instruction.condition):
            registers[instruction.register] += instruction.value

            max_value = max(max_value, highest_register_value(registers))

    return registers, max_value


def highest_register_value(registers: dict[str, int]) -> int:
    return max(registers.values())


def parse(input: str) -> list[Instruction]:
    instructions = []
    for line in input.splitlines():
        register, operation, value, condition_register, condition = (
            INSTRUCTION_PATTERN.match(line).groups()
        )

        match operation:
            case "inc":
                value = int(value)
            case "dec":
                value = -int(value)

        instructions.append(Instruction(register, value, condition_register, condition))

    return instructions
