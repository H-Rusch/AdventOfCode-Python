from collections import defaultdict
from multiprocessing import Queue, Process, Value
from queue import Empty


class SoundCard:
    def __init__(self, instructions: list) -> None:
        self.instructions = instructions
        self.registers = defaultdict(int)
        self.ic = 0
        self.last_frequency = None
        self.halt = False

    def execute_program(self):
        while self.ic in range(len(self.instructions)) and not self.halt:
            instruction = self.instructions[self.ic]
            try:
                self.ic += self.execute_instruction(*instruction)
            except Empty:
                self.halt = True

    def execute_instruction(self, operation: str, arg1: str, arg2: str = None) -> int:
        match operation:
            case "snd":
                self.last_frequency = self.get_value(arg1)
            case "set":
                self.registers[arg1] = self.get_value(arg2)
            case "add":
                self.registers[arg1] += self.get_value(arg2)
            case "mul":
                self.registers[arg1] *= self.get_value(arg2)
            case "mod":
                self.registers[arg1] = self.registers[arg1] % self.get_value(arg2)
            case "rcv":
                if self.get_value(arg1) != 0:
                    self.halt = True
            case "jgz":
                if self.get_value(arg1) > 0:
                    return self.get_value(arg2)
            case _:
                raise ValueError(f"Operation not supported: {operation}")

        return 1

    def get_value(self, value: str) -> int:
        if value.lstrip("-").isnumeric():
            return int(value)
        return self.registers[value]


class ParallelSoundCard(SoundCard):
    def __init__(self, instructions: list, id: int) -> None:
        super().__init__(instructions)
        self.registers["p"] = id
        self.receiving = Queue()
        self.send_count = Value("i", 0)
        self.other = None

    def execute_instruction(self, operation: str, arg1: str, arg2: str = None) -> int:
        match operation:
            case "snd":
                self.other.receiving.put(self.get_value(arg1))
                self.send_count.value += 1
            case "set":
                self.registers[arg1] = self.get_value(arg2)
            case "add":
                self.registers[arg1] += self.get_value(arg2)
            case "mul":
                self.registers[arg1] *= self.get_value(arg2)
            case "mod":
                self.registers[arg1] = self.registers[arg1] % self.get_value(arg2)
            case "rcv":
                # This timeout is tested for my machine. It might need to be adjusted upwards on slower hadware
                self.registers[arg1] = self.receiving.get(timeout=0.1)
            case "jgz":
                if self.get_value(arg1) > 0:
                    return self.get_value(arg2)
            case _:
                raise ValueError(f"Operation not supported: {operation}")

        return 1


def part1(input):
    instructions = parse(input)

    card = SoundCard(instructions)
    card.execute_program()

    return card.last_frequency


def part2(input):
    instructions = parse(input)

    card1 = ParallelSoundCard(instructions, 0)
    card2 = ParallelSoundCard(instructions, 1)
    card1.other = card2
    card2.other = card1

    processes = [Process(target=card.execute_program) for card in (card1, card2)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()

    return int(card2.send_count.value)


def parse(input: str) -> list[list[str]]:
    return [line.split() for line in input.splitlines()]
