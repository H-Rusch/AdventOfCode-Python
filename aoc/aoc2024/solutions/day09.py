from abc import ABC
from collections import deque


class Block(ABC):
    def __init__(self, amount: int):
        self.amount = amount


class File(Block):
    def __init__(self, id: int, amount: int):
        super().__init__(amount)
        self.id = id

    def score_of_full_file(self, offset: int) -> int:
        return sum((offset + n) * self.id for n in range(self.amount))

    def __repr__(self):
        return " ".join([str(self.id) for _ in range(self.amount)])


class Empty(Block):
    def __repr__(self):
        return " ".join(["." for _ in range(self.amount)])


def part1(input: str) -> int:
    blocks = parse(input)

    result = 0
    offset = 0
    index = 0
    while index < len(blocks):
        block = blocks[index]

        if isinstance(block, File):
            result += block.score_of_full_file(offset)
            offset += block.amount
        else:
            for _ in range(block.amount):
                file = find_rightmost_file(blocks, index)
                if file is None:
                    break

                result += offset * file.id
                offset += 1

                file.amount -= 1

        index += 1

    return result


def find_rightmost_file(blocks: deque[Block], index: int) -> File | None:
    while len(blocks) > index:
        if blocks[-1].amount == 0 or isinstance(blocks[-1], Empty):
            blocks.pop()
        else:
            return blocks[-1]

    return None


def part2(input: str) -> int:
    blocks = parse(input)

    right = len(blocks) - 1
    while right > 1:
        same_length = relocate_file(blocks, right)
        right -= same_length

    # tally score
    result = 0
    offset = 0
    for block in blocks:
        if isinstance(block, File):
            result += block.score_of_full_file(offset)
        offset += block.amount

    return result


def relocate_file(blocks: list[Block], right: int) -> bool:
    """Return whether a new empty block was inserted to keep track during iteration"""
    file_index = find_file_to_relocate(blocks, right)
    empty_index = find_first_fitting_empty(blocks, file_index)
    if empty_index is None:
        return True

    # replace block with file followed by remaining empty blocks
    file = blocks[file_index]
    empty_block = blocks[empty_index]
    new_empty_index = empty_index + 1
    leftover_empty_amount = empty_block.amount - file.amount

    blocks[file_index] = Empty(file.amount)
    blocks[empty_index] = file
    if leftover_empty_amount > 0:
        blocks.insert(new_empty_index, Empty(leftover_empty_amount))
        return False
    return True


def find_file_to_relocate(blocks: list[Block], right: int) -> int | None:
    while right > 0:
        if isinstance(blocks[right], File):
            return right
        right -= 1


def find_first_fitting_empty(blocks: list[Block], file_index: int) -> int | None:
    file = blocks[file_index]
    index = 0
    while index < file_index:
        if isinstance(blocks[index], Empty) and blocks[index].amount >= file.amount:
            return index
        index += 1


def print_blocks(blocks):
    print(" ".join(map(str, blocks)))


def parse(input: str) -> deque[Block]:
    def parse_block(i: int, digit: str) -> Block:
        digit = int(digit)
        if i % 2 == 0:
            return File(i // 2, digit)
        else:
            return Empty(digit)

    return deque([parse_block(i, digit) for i, digit in enumerate(input)])
