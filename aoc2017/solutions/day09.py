class GroupParser:
    def __init__(self, input: str) -> None:
        self.input = input
        self.index = 0

        self.score = 0
        self.depth = 0

        self.garbage = False
        self.garbage_filtered = 0

    def parse(self):
        while self.index < len(self.input):
            self.process_letter()
            self.index += 1

    def process_letter(self):
        letter = self.input[self.index]

        if letter == "!":
            self.index += 1
            return

        if self.garbage:
            self.process_garbage(letter)
        else:
            self.process_normal(letter)

    def process_garbage(self, letter: str):
        match letter:
            case ">":
                self.garbage = False
            case _:
                self.garbage_filtered += 1

    def process_normal(self, letter: str):
        match letter:
            case "{":
                self.depth += 1
                self.score += self.depth
            case "<":
                self.garbage = True
            case "}":
                self.depth -= 1
            case _:
                pass


def part1(input):
    parser = GroupParser(input)
    parser.parse()

    return parser.score


def part2(input):
    parser = GroupParser(input)
    parser.parse()

    return parser.garbage_filtered
