LIMIT = 50_000_000


class Spinlock:
    def __init__(self, step_size: int) -> None:
        self.step_size = step_size
        self.numbers = [0]
        self.index = 0

    def insert_next(self):
        insert_value = self.numbers[self.index] + 1
        self.index = (self.index + self.step_size) % len(self.numbers) + 1

        self.numbers.insert(self.index, insert_value)


def part1(input):
    spinlock = Spinlock(int(input))

    return execute_part1(spinlock)


def execute_part1(spinlock: Spinlock) -> int:
    for _ in range(2017):
        spinlock.insert_next()

    return spinlock.numbers[spinlock.index + 1]


def part2(input):
    "Simulate the spinlocks functionality without actually inserting values."
    step_size = int(input)
    index = 0
    value_after_zero = None

    for i in range(1, LIMIT + 1):
        index = (index + step_size) % i + 1
        if index == 1:
            value_after_zero = i

    return value_after_zero
