from functools import reduce


class KnotHash:
    ROUNDS = 64
    CAPACITY = 256

    @classmethod
    def hash(self, input: str):
        lengths = adjust_input(input)
        performer = KnotHashPerformer(lengths, KnotHash.CAPACITY)

        performer.perform_rounds(KnotHash.ROUNDS)
        dense_hash = performer.dense_hash()

        return KnotHash.dense_hash_repr(dense_hash)

    @classmethod
    def dense_hash_repr(cls, dense_hash: list[int]) -> str:
        def num_to_hex(number: int) -> str:
            return hex(number)[2:].zfill(2)

        return "".join(map(num_to_hex, dense_hash))


class KnotHashPerformer:
    BLOCK_SIZE = 16

    def __init__(self, lengths: list[int], capacity: int = 256) -> None:
        self.numbers = [n for n in range(capacity)]
        self.lengths = lengths
        self.index = 0
        self.skip_size = 0

    def perform_rounds(self, rounds: int):
        for _ in range(rounds):
            self.perform_round()

    def perform_round(self):
        for length in self.lengths:
            reverse(self.numbers, self.index, int(length))
            self.index = (self.index + length + self.skip_size) % len(self.numbers)
            self.skip_size += 1

    def dense_hash(self):
        blocks = [
            self.numbers[
                i * KnotHashPerformer.BLOCK_SIZE : (i + 1)
                * KnotHashPerformer.BLOCK_SIZE
            ]
            for i in range(KnotHashPerformer.BLOCK_SIZE)
        ]
        return list(map(lambda block: reduce(lambda v1, v2: v1 ^ v2, block), blocks))


def part1(input):
    return execute_part1(input, 256)


def execute_part1(input: str, capacity: int) -> int:
    lengths = [int(n) for n in input.split(",")]

    performer = KnotHashPerformer(lengths, capacity)
    performer.perform_round()

    return performer.numbers[0] * performer.numbers[1]


def part2(input):
    return KnotHash.hash(input)


def reverse(numbers: list, start_index: int, length: int):
    offset = 0
    while offset < length / 2:
        current_index = (start_index + offset) % len(numbers)
        target_index = (start_index + length - offset - 1) % len(numbers)

        numbers[current_index], numbers[target_index] = (
            numbers[target_index],
            numbers[current_index],
        )

        offset += 1


def adjust_input(input: str) -> list:
    processed = process_input(input)
    processed.extend([17, 31, 73, 47, 23])

    return processed


def process_input(input: str) -> list:
    return [ord(c) for c in input]
