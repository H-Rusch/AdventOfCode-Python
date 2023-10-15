from functools import reduce

class KnotHash:
    BLOCK_SIZE = 16

    def __init__(self, lenghts: list[int], capacity: int = 256) -> None:
        self.numbers = [n for n in range(capacity)]
        self.lengths = lenghts
        self.index = 0
        self.skip_size = 0

    def hash(self):
        self.perform_rounds(64)
        dense_hash = self.dense_hash()

        return KnotHash.dense_hash_repr(dense_hash)

    def perform_rounds(self, rounds: int):
        for _ in range(rounds):
            self.perform_round()

    def perform_round(self):
        for length in self.lengths:
            reverse(self.numbers, self.index, int(length))
            self.index = (self.index + length + self.skip_size) % len(self.numbers)
            self.skip_size += 1

    def dense_hash(self):
        blocks = [self.numbers[i * KnotHash.BLOCK_SIZE: (i + 1) * KnotHash.BLOCK_SIZE] for i in range(KnotHash.BLOCK_SIZE)]
        return list(map(lambda block: reduce(lambda v1, v2: v1^v2, block), blocks))

    @classmethod
    def dense_hash_repr(cls, dense_hash: list[int]) -> str:
        def num_to_hex(number: int) -> str:
            return hex(number)[2:].zfill(2)
        
        return "".join(map(num_to_hex, dense_hash))


def part1(input):
    return execute_part1(input, 256)


def execute_part1(input: str, capacity: int) -> int:
    lengths = [int(n) for n in input.split(",")]

    knotHash = KnotHash(lengths, capacity)
    knotHash.perform_round()

    return knotHash.numbers[0] * knotHash.numbers[1]


def part2(input):
    lengths = adjust_input(input)
    knotHash = KnotHash(lengths, 256)
    
    return knotHash.hash()


def reverse(numbers: list, start_index: int, length: int):
    offset = 0
    while offset < length / 2:
        current_index = (start_index + offset) % len(numbers)
        target_index = (start_index + length - offset - 1) % len(numbers)

        numbers[current_index], numbers[target_index] = numbers[target_index], numbers[current_index]

        offset += 1


def adjust_input(input: str) -> list:
    processed = process_input(input)
    processed.extend([17, 31, 73, 47, 23])

    return processed


def process_input(input: str) -> list:
    return [ord(c) for c in input]
