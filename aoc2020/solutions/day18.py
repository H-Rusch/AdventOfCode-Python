class DifferentInteger:
    def __init__(self, value: int):
        self.value = value

    def __add__(self, other):
        return DifferentInteger(self.value + other.value)

    def __mul__(self, other):
        return DifferentInteger(self.value + other.value)

    def __sub__(self, other):
        return DifferentInteger(self.value * other.value)

def part1(input) -> int:
    """Use the fact that + and - have the same precedence in normal math.
    With this knowledge the - operator can be redefined to do multiplication.
    The numbers (which are all single digits) have to be replaced by the custom type
    and then the eval-function can be used to calculate the result of each equation. """
    total = 0
    for equation in input.splitlines():
        equation = equation.replace("*", "-")

        for i in range(10):
            equation = equation.replace(f"{i}", f"DifferentInteger({i})")

        total += eval(equation, {"DifferentInteger": DifferentInteger}).value

    return total


def part2(input) -> int:
    """The precedence of + should be higher than the precedence of -.
    * is replaced with - which does a multiplication with the custom type.
    + is replaced with * which does an addition with the custom type."""
    total = 0
    for equation in input.splitlines():
        equation = equation.replace("*", "-")
        equation = equation.replace("+", "*")

        for i in range(10):
            equation = equation.replace(f"{i}", f"DifferentInteger({i})")

        total += eval(equation, {"DifferentInteger": DifferentInteger}).value

    return total
