from functools import cache


class Program:
    "Tree structure with knowledge of the parent element."

    def __init__(self, name: str, weight: int):
        self.name = name
        self.weight = weight
        self.children = []
        self.parent = None

    def calculate_weight(self) -> int:
        if len(self.children) == 0:
            return self.weight

        return self.weight + sum(self.calculate_children_weights())

    @cache
    def calculate_children_weights(self) -> list[int]:
        return list(map(Program.calculate_weight, self.children))

    def is_balanced(self) -> bool:
        weights = self.calculate_children_weights()

        return all(weight == weights[0] for weight in weights)


def part1(input):
    root = parse(input)

    return root.name


def part2(input):
    root = parse(input)

    node = root
    while node is not None:
        if not node.is_balanced() and all(map(Program.is_balanced, node.children)):
            full_weights = node.calculate_children_weights()

            outlier_weight, normal_weight = find_outlier_weight(full_weights)
            diff = normal_weight - outlier_weight
            outlier_node = find_outlier_node(node.children, outlier_weight)

            return outlier_node.weight + diff

        for child in node.children:
            if not child.is_balanced():
                node = child


def find_outlier_weight(numbers: list[int]) -> (int, int):
    number_count = {number: numbers.count(number) for number in numbers}

    for number in numbers:
        if number_count[number] == 1:
            outlier = number
        else:
            normal = number

    return outlier, normal


def find_outlier_node(nodes: list[Program], outlier_weight: int) -> Program:
    return list(filter(lambda node: node.calculate_weight() == outlier_weight, nodes))[
        0
    ]


def parse(input: str) -> Program:
    programs = dict()

    create_initial_nodes(programs, input)
    connect_nodes(programs, input)

    return find_root(programs.values())


def create_initial_nodes(programs: dict[str, Program], input: str):
    for line in input.splitlines():
        parts = line.split()
        name = parts[0]
        weight = int(parts[1][1:-1])

        programs[name] = Program(name, weight)


def connect_nodes(programs: dict[str, Program], input: str):
    for line in input.splitlines():
        parts = line.split()
        if len(parts) <= 2:
            continue

        name = parts[0]
        children = parts[3:]
        program = programs[name]

        for child in children:
            child = child.rstrip(",")
            child_program = programs[child]
            program.children.append(child_program)
            child_program.parent = program


def find_root(programs: list[Program]) -> Program:
    for program in programs:
        if program.parent == None:
            return program
