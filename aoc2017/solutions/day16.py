LIMIT = 1_000_000_000


class Dance:
    def __init__(self, program_count: int) -> None:
        self.programs = [chr(i + ord("a")) for i in range(program_count)]

    def spin(self, x: int):
        self.programs = self.programs[-x:] + self.programs[:-x]

    def exchange(self, index1: int, index2: int):
        self.programs[index1], self.programs[index2] = self.programs[index2], self.programs[index1]

    def partner(self, program1: str, program2: str):
        index1 = self.programs.index(program1)
        index2 = self.programs.index(program2)

        self.exchange(index1, index2)

    def __str__(self) -> str:
        return "".join(self.programs)


def part1(input):
    dance = Dance(16)
    return perform_dance(dance, input.split(","))


def part2(input):
    dance = Dance(16)
    instructions = input.split(",")

    i = 0
    states = {}
    while True:
        state = perform_dance(dance, instructions)
        if state in states:
            return shortcut_to_limit(states, state, i)

        states[state] = i
        i += 1


def perform_dance(dance: Dance, instructions: list[str]) -> str:
    for instruction in instructions:
        move = instruction[0]
        if move == "s":
            dance.spin(int(instruction[1:]))
        elif move == "x":
            index1, index2 = (int(n) for n in instruction[1:].split("/"))
            dance.exchange(index1, index2)
        elif move == "p":
            program1, program2 = instruction[1:].split("/")
            dance.partner(program1, program2)

    return str(dance)


def shortcut_to_limit(states: dict[str, int], state: str, i: int) -> str:
    offset = (LIMIT % (i - states[state]) - states[state]) - 1
    for key, value in states.items():
        if value == offset:
            return key
