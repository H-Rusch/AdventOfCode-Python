class Node:
    def __init__(self):
        self.children = []
        self.metadata = []

    def sum_metadata(self):
        summed = sum(self.metadata)
        for child in self.children:
            summed += child.sum_metadata()

        return summed

    def calculate_value(self):
        if len(self.children) == 0:
            return sum(self.metadata)
        else:
            value = 0
            for index in self.metadata:
                if index == 0 or index > len(self.children):
                    continue
                value += self.children[index - 1].calculate_value()

            return value


class CountHolder:
    def __init__(self, num: int):
        self._num = num

    @property
    def num(self):
        val = self._num
        self._num += 1

        return val


def part1(input: str) -> int:
    root = parse(input)

    return root.sum_metadata()


def part2(input: str) -> int:
    root = parse(input)

    return root.calculate_value()


def build_node(numbers: list, index: CountHolder) -> Node:
    """Build nodes recursively. Index holds reference to the current position in the list of numbers."""
    node = Node()
    num_children = numbers[index.num]
    num_metadata = numbers[index.num]

    for _ in range(num_children):
        node.children.append(build_node(numbers, index))
    for _ in range(num_metadata):
        node.metadata.append(numbers[index.num])

    return node


def parse(input):
    numbers = [int(s) for s in input.split()]

    return build_node(numbers, CountHolder(0))
