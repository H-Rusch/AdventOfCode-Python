import math
import copy
from itertools import permutations


class Node:
    def __init__(self, value: int = None, parent=None):
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None

    def to_string(self):
        # for debug purposes
        if self.value is not None:
            return str(self.value)
        else:
            return "[" + self.left.to_string() + "," + self.right.to_string() + "]"


def part1(input: str) -> int:
    nodes = parse(input)

    while len(nodes) > 1:
        # add the first two numbers in the list
        parent = Node()
        node_1 = nodes.pop(0)
        node_2 = nodes.pop(0)
        node_1.parent = parent
        node_2.parent = parent
        parent.left = node_1
        parent.right = node_2

        # reduce the sum
        reduce(parent)

        # add the sum in the front of the list
        nodes.insert(0, parent)

    return calculate_magnitude(nodes[0])


def part2(input: str) -> int:
    nodes = parse(input)

    max_magnitude = 0
    for n1, n2 in permutations(nodes, 2):
        parent = Node()
        n1 = copy.deepcopy(n1)
        n2 = copy.deepcopy(n2)
        n1.parent, n2.parent = parent, parent
        parent.left, parent.right = n1, n2

        reduce(parent)
        magnitude = calculate_magnitude(parent)

        if magnitude > max_magnitude:
            max_magnitude = magnitude

    return max_magnitude


def calculate_magnitude(node: Node) -> int:
    if node.value is not None:
        return node.value

    return 3 * calculate_magnitude(node.left) + 2 * calculate_magnitude(node.right)


def reduce(node: Node):
    while True:
        to_explode = need_explode(node)
        if to_explode is not None:
            explode(to_explode)
            continue

        to_split = need_split(node)
        if to_split is not None:
            split(to_split)
            continue

        break


def need_explode(node: Node, depth: int = 0) -> Node:
    if node is None:
        return None

    # node which needs to be exploded found
    if node.left is not None and depth == 4:
        return node

    # search left subtree
    result_left = need_explode(node.left, depth + 1)
    if result_left is not None:
        return result_left

    # search right subtree
    result_right = need_explode(node.right, depth + 1)
    if result_right is not None:
        return result_right


def explode(node: Node):
    value_left = node.left.value
    value_right = node.right.value

    first_left = first_regular_value(node.parent, node, True)
    if first_left is not None:
        first_left.value += value_left

    first_right = first_regular_value(node.parent, node, False)
    if first_right is not None:
        first_right.value += value_right

    node.left, node.right = None, None
    node.value = 0


def first_regular_value(node: Node, start: Node, left: bool) -> Node:
    """
    Find the first node which has a regular value or None if there is none.
    The parameter 'left' the direction can be controlled. 'True' searches on the left. 'False' searches on the right.
    When searching for the first value on the right, the right 'super'-trees have to be checked for their left most value.
    """
    if node is None:
        return None

    # search left/ right subtree
    if left and node.left != start:
        found = search_right_first(node.left)
        if found is not None:
            return found

    elif not left and node.right != start:
        found = search_left_first(node.right)
        if found is not None:
            return found

    # search parent
    return first_regular_value(node.parent, node, left)


def search_right_first(node: Node) -> Node:
    """Search through a tree for a value always considering the right subtree first."""
    # first regular value reached
    if node.value is not None:
        return node

    a = search_right_first(node.right)
    if a is not None:
        return a
    return search_right_first(node.left)


def search_left_first(node: Node) -> Node:
    """Search through a tree for a value always considering the left subtree first."""
    # first regular value reached
    if node.value is not None:
        return node

    a = search_left_first(node.left)
    if a is not None:
        return a
    return search_right_first(node.right)


def need_split(node: Node) -> Node:
    if node is None:
        return None

    if node.value is not None and node.value >= 10:
        return node

    # search left subtree
    result_left = need_split(node.left)
    if result_left is not None:
        return result_left

    # search right subtree
    result_right = need_split(node.right)
    if result_right is not None:
        return result_right


def split(node: Node):
    left_value = math.floor(node.value / 2)
    right_value = math.ceil(node.value / 2)

    left_child = Node(value=left_value, parent=node)
    right_child = Node(value=right_value, parent=node)

    node.value = None
    node.left = left_child
    node.right = right_child


def create_tree(line: list, parent: Node = None):
    # bottom reached
    if len(line) == 1:
        node = Node(value=int(line[0]), parent=parent)
        return node

    # go further down
    opening, closing, comma = find_next_part(line)

    node = Node(parent=parent)
    left_part = line[:comma]
    right_part = line[comma + 1:]

    if opening is not None:
        left_part.pop("".join(left_part).find("["))
        right_part.pop("".join(right_part).rfind("]"))

    node.left = create_tree(left_part, node)
    node.right = create_tree(right_part, node)

    return node


def find_next_part(line: list) -> tuple:
    """
    Find top level opening and closing block. Return the indices of where the brackets open and close and where
    the element is separated.
    """
    opening, closing, comma = None, None, None
    depth = 0

    for i in range(len(line)):
        if line[i] == "[":
            if depth == 0:
                opening = i
            depth += 1

        elif line[i] == "]":
            depth -= 1
            if depth == 0:
                closing = i

        elif line[i] == ",":
            if depth == 1:
                comma = i

    return opening, closing, comma


def parse(input: str):
    nodes = []
    for line in input.splitlines():
        parts = [line[i] for i in range(len(line))]
        root = create_tree(parts)
        nodes.append(root)

    return nodes
