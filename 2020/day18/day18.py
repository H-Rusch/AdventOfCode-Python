class DifferentInteger:
    def __init__(self, value: int):
        self.value = value

    def __add__(self, other):
        return DifferentInteger(self.value + other.value)

    def __mul__(self, other):
        return DifferentInteger(self.value + other.value)

    def __sub__(self, other):
        return DifferentInteger(self.value * other.value)

def part_1(equations: list) -> int:
    """Use the fact that + and - have the same precedence in normal math.
    With this knowledge the - operator can be redefined to do multiplication.
    The numbers (which are all single digits) have to be replaced by the custom type
    and then the eval-function can be used to calculate the result of each equation. """
    total = 0
    for equation in equations:
        equation = equation.replace("*", "-")

        for i in range(10):
            equation = equation.replace(f"{i}", f"DifferentInteger({i})")

        total += eval(equation, {"DifferentInteger": DifferentInteger}).value

    return total


def part_2(equations: list) -> int:
    """The precedence of + should be higher than the precedence of -.
    * is replaced with - which does a multiplication with the custom type.
    + is replaced with * which does an addition with the custom type."""
    total = 0
    for equation in equations:
        equation = equation.replace("*", "-")
        equation = equation.replace("+", "*")

        for i in range(10):
            equation = equation.replace(f"{i}", f"DifferentInteger({i})")

        total += eval(equation, {"DifferentInteger": DifferentInteger}).value

    return total


def parse_inputs():
    with open("input.txt") as file:
        return file.read().splitlines()


if __name__ == "__main__":
    equation_list = parse_inputs()

    print(f"Part 1: The sum of all equations is {part_1(equation_list)}.")

    print(f"Part 2: With advanced mathematics the sum of all equations is {part_2(equation_list)}.")
