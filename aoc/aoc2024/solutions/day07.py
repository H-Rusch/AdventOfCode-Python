from dataclasses import dataclass
from typing import Callable


@dataclass
class Equation:
    result: int
    values: list[int]

    @staticmethod
    def from_str(line: str) -> "Equation":
        result, values = line.split(": ")

        return Equation(int(result), list(map(int, values.split())))

    def can_be_fulfilled(self) -> bool:
        operations = [
            lambda x, y: x + y,
            lambda x, y: x * y,
        ]
        return self._helper(self.values[0], 1, operations)

    def can_be_fulfilled_complex(self) -> bool:
        operations = [
            lambda x, y: x + y,
            lambda x, y: x * y,
            lambda x, y: int(str(x) + str(y)),
        ]
        return self._helper(self.values[0], 1, operations)

    def _helper(
        self, current: int, index: int, operations: list[Callable[[int, int], int]]
    ):
        if current > self.result:
            return False

        if index >= len(self.values):
            return current == self.result

        value = self.values[index]
        # using any() here is about 100% slower thatn just using plain or operations (1,1s -> 2,4s)
        # my goal was to reduce duplication though
        return any(
            (
                self._helper(operation(current, value), index + 1, operations)
                for operation in operations
            )
        )


def part1(input: str) -> int:
    equations = parse(input)

    fulfillable_equations = filter(Equation.can_be_fulfilled, equations)
    return sum(map(lambda x: x.result, fulfillable_equations))


def part2(input: str) -> int:
    equations = parse(input)

    fulfillable_equations = filter(Equation.can_be_fulfilled_complex, equations)
    return sum(map(lambda x: x.result, fulfillable_equations))


def parse(input: str) -> list[Equation]:
    return [Equation.from_str(line) for line in input.splitlines()]
