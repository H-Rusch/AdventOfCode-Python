import regex


def part1(rules: str, messages: str) -> int:
    reg = regex.compile(build_regex_string(rules))

    return sum([bool(reg.fullmatch(message)) for message in messages.splitlines()])


def part2(rules: str, messages: str) -> int:
    reg = regex.compile(build_regex_string(rules, recursive=True))

    return sum([bool(reg.fullmatch(message)) for message in messages.splitlines()])


def build_regex_string(rules: str, recursive=False) -> str:
    grammar = dict([line.split(": ") for line in rules.splitlines()])

    def dfs(lit="0"):
        if grammar[lit][0] == '"':
            return grammar[lit][1]

        if recursive:
            if lit == "8":
                return dfs("42") + "+"
            elif lit == "11":
                # the full group is named "pumping" with the "?P<pumping>" in the beginning.
                # this group can recursively be repeated with the "(?P&pumping)?" near the middle
                return f'(?P<pumping>{dfs("42")}(?P&pumping)?{dfs("31")})'


        # list comprehension of the following loop found below
        # s = ""
        # for alt in grammar[lit].split("|"):
        #    for part in alt.split():
        #        s += dfs(part)
        #    s += "|"
        # s = s[:-1]
        branches = "|".join(
            ["".join([dfs(part) for part in alt.split()]) for alt in grammar[lit].split("|")]
        )
        return "(" + branches + ")"

    return "^" + dfs() + "$"


def parse(input):
    with open("input.txt") as file:
        return file.read().split("\n\n")


if __name__ == "__main__":
    rule_part, message_part = parse(input)

    print(f"Part 1: {part1(rule_part, message_part)} messages match the rules.")

    print(f"Part 2: {part2(rule_part, message_part)} messages match the new rules.")
