# very interesting approach for this problem posted by /u/petter_s

import re


class Equation:
    def __init__(self, string: str):
        self.terms = re.findall(r"\d+|\+|\*|\(|\)", string)
        self.index = 0

    def evaluate(self) -> int:
        """
        Calculate the leftmost term first. Then step through the remaining terms and as long as + or * is found, add or
        multiply the current result with the next term.
        """
        result = self.evaluate_term()
        self.consume(")")

        while True:
            if self.consume("+"):
                result += self.evaluate_term()
            elif self.consume("*"):
                result *= self.evaluate_term()
            else:
                break

        return result

    def evaluate_term(self) -> int:
        """
        Handle a term put in brackets with priority and calculate its full result.
        If no leading bracket was found in the next term, it is a digit.
        """
        if self.consume("("):
            sub_result = self.evaluate()
            self.consume(")")

            return sub_result
        else:
            return int(self.next())

    def consume(self, term: str) -> bool:
        """Move along the list of terms, if the given term is currently active. """
        if self.index < len(self.terms) and self.terms[self.index] == term:
            self.next()

            return True
        else:
            return False

    def next(self) -> str:
        self.index += 1

        return self.terms[self.index - 1]


class Equation2(Equation):
    def evaluate(self) -> int:
        """Now the + sign has a higher priority. For that reason each new term has to evaluate the additions first. """
        result = self.evaluate_sum()
        while self.consume("*"):
            result *= self.evaluate_sum()

        return result

    def evaluate_sum(self) -> int:
        result = self.evaluate_term()
        while self.consume("+"):
            result += self.evaluate_term()

        return result


def part_1(equations: list) -> int:
    return sum([Equation(equation).evaluate() for equation in equations])


def part_2(equations: list) -> int:
    return sum([Equation2(equation).evaluate() for equation in equations])


def parse_inputs():
    with open("input.txt") as file:
        return file.read().splitlines()


if __name__ == "__main__":
    equation_list = parse_inputs()

    print(f"Part 1: The sum of all equations is {part_1(equation_list)}.")

    print(f"Part 2: With advanced mathematics the sum of all equations is {part_2(equation_list)}.")
