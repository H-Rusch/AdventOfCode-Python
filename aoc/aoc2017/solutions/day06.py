class Memory:
    def __init__(self, banks: list[int]) -> None:
        self.banks = banks

    def rebalance(self):
        rebalance_index = self.rebalance_candidate_index()
        rebalance_amount = self.banks[rebalance_index]
        self.banks[rebalance_index] = 0

        for i in range(1, rebalance_amount + 1):
            index = (rebalance_index + i) % len(self.banks)
            self.banks[index] += 1

    def rebalance_candidate_index(self) -> int:
        max_value = max(self.banks)
        return self.banks.index(max_value)

    def state(self):
        return ", ".join([str(n) for n in self.banks])


def part1(input):
    initial_counts = parse(input)

    memory = Memory(initial_counts)

    return find_first_repeating_state(memory)


def part2(input):
    initial_counts = parse(input)

    memory = Memory(initial_counts)
    find_first_repeating_state(memory)

    return find_repeating(memory, memory.state())


def find_first_repeating_state(memory: Memory) -> (int, str):
    unique_states = set()
    count = 0

    while True:
        state = memory.state()
        if state in unique_states:
            return count

        unique_states.add(state)

        memory.rebalance()
        count += 1


def find_repeating(memory: Memory, repeating_state: str) -> int:
    count = 0

    while True:
        memory.rebalance()
        count += 1

        state = memory.state()
        if state == repeating_state:
            return count


def parse(input):
    return [int(n) for n in input.split()]
