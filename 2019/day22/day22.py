import re


class Deck:
    def __init__(self):
        self.start = None
        self.end = None
        self.cards = []

    def generate_deck(self, size: int):
        i = 0
        self.cards.append(Card(i))
        while i < size - 1:
            i += 1
            current = Card(i)
            current.previous = self.cards[-1]
            self.cards[-1].next = current
            self.cards.append(current)

        self.start = self.cards[0]
        self.end = self.cards[-1]
        self.end.next = self.start
        self.start.previous = self.end

    def new_stack(self):
        current = self.start

        while True:
            # swap previous and next for each card
            tmp = current.next
            current.next = current.previous
            current.previous = tmp

            current = current.previous

            if current is self.start:
                break

        # swap start and end of the deck
        tmp = self.start
        self.start = self.end
        self.end = tmp

    def cut(self, n: int):
        if n > 0:
            current = self.start
            for _ in range(n - 1):
                current = current.next

            self.start = current.next
            self.end = current
        elif n < 0:
            current = self.end
            for _ in range(abs(n) - 1):
                current = current.previous

            self.start = current
            self.end = current.previous

    def deal_with_increment(self, n: int):
        # bring the cards in the correct order
        cards = [None for _ in range(len(self.cards))]
        i = 0
        current = self.start

        while True:
            cards[i] = current
            current = current.next

            i = (i + n) % len(cards)

            if current is self.start:
                break

        # fix next and previous pointers
        self.start = cards[0]
        self.end = cards[-1]
        self.start.previous = self.end
        self.end.next = self.start
        current = self.start
        i = 0
        while i < len(cards) - 1:
            current.next = cards[i + 1]
            cards[i + 1].previous = current

            current = current.next
            i += 1

    def index_of_value(self, value: int) -> int:
        if value >= len(self.cards):
            return -1

        current = self.start
        i = 0
        while current.value != value:
            i += 1
            current = current.next

        return i

    def print_values(self):
        current = self.start
        while True:
            print(current.value)
            current = current.next

            if current is self.start:
                break


class Card:
    def __init__(self, value: int):
        self.value = value
        self.next = None
        self.previous = None


def part1(instructions: list) -> int:
    deck = Deck()
    deck.generate_deck(10_007)

    for inst in instructions:
        if inst.startswith("cut"):
            deck.cut(int(re.search(r"-?\d+", inst).group(0)))
        elif inst.startswith("deal into"):
            deck.new_stack()
        else:
            deck.deal_with_increment(int(re.search(r"-?\d+", inst).group(0)))

    return deck.index_of_value(2019)


def parse(input) -> list:
    with open("input.txt", "r") as file:
        return file.readlines()


if __name__ == "__main__":
    instruction_list = parse(input)

    print(f"Part 1: Card 2019 is at position {part1(instruction_list)}.")
