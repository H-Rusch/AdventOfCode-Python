def find_matching_parenthesis(equation: str):
    depth = 0
    for i in range(1, len(equation) + 1):
        if equation[-i] == ")":
            depth += 1
        elif equation[-i] == "(":
            depth -= 1
            if depth == 0:
                return -i


def solve_equation(equation: str):
    i = 1
    while i != len(equation):
        if equation[-i] == ")":
            opening = find_matching_parenthesis(equation)
            equation = equation[:opening] + str(solve_equation(equation[opening + 1:-i]))
            i = 0
        if equation[-i] == "+":
            return int(equation[-i + 1:]) + solve_equation(equation[:-i])
        elif equation[-i] == "*":
            return int(equation[-i + 1:]) * solve_equation(equation[:-i])

        i += 1
    return int(equation.replace(")", ""))


# read in equations
with open("input.txt", "r") as file:
    equations = [equation.replace(" ", "") for equation in file.read().split("\n")]

sum_of_equation = 0
for eq in equations:
    sum_of_equation += solve_equation(eq)

print(sum_of_equation)
