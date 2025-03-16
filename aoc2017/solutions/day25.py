from collections import defaultdict
import re


TRANSFORMATION_REGEX = re.compile(r"""In state (.*?):
  If the current value is (0):
    - Write the value (0|1)\.
    - Move one slot to the (right|left)\.
    - Continue with state (.*?)\.
  If the current value is (1):
    - Write the value (0|1)\.
    - Move one slot to the (left|right).
    - Continue with state (.*?)\.""")


class TuringMachine:
    def __init__(self, state: str, transitions: dict) -> None:
        self.tape = defaultdict(int)
        self.position = 0
        self.state = state
        self.transitions = transitions

    def next_state(self):
        key = (self.state, self.tape[self.position])
        next_state, write, move = self.transitions[key]

        self.state = next_state
        self.tape[self.position] = write
        self.position += move

    def diagnostic_checksum(self) -> int:
        return sum(self.tape.values())


def part1(input):
    inital_state, steps, transitions = parse(input)
    tm = TuringMachine(inital_state, transitions)

    for _ in range(steps):
        tm.next_state()

    return tm.diagnostic_checksum()


def part2(_):
    return "No second puzzle on the last day 💻"


def parse(input) -> (str, int, dict):
    transitions = {}
    parts = input.split("\n\n")
    preamble = parts[0].splitlines()
    initial_state = preamble[0][15]
    steps = int(
        preamble[1]
        .removeprefix("Perform a diagnostic checksum after ")
        .removesuffix(" steps.")
    )

    for part in parts[1:]:
        parse_state(transitions, part)

    return initial_state, steps, transitions


def parse_state(transitions: dict, part: str):
    groups = TRANSFORMATION_REGEX.match(part).groups()
    state = groups[0]

    size = 4
    for i in (0, 1):
        current_value, write, move, next_state = groups[
            1 + i * size : 1 + size + i * size
        ]
        current_value = int(current_value)
        write = int(write)
        move = move_value(move)

        key = (state, current_value)
        value = (next_state, write, move)

        transitions[key] = value


def move_value(move: str) -> int:
    match move:
        case "right":
            return 1
        case "left":
            return -1
