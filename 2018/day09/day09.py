from collections import defaultdict
import re


class Marble:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


class MarbleGame:
    def __init__(self, max_players, limit):
        self.current = Marble(0)
        self.current.next = self.current
        self.current.prev = self.current

        self.scores = defaultdict(int)
        self.player = 0
        self.max_players = max_players
        self.limit = limit

    def play_game(self):
        for i in range(1, self.limit):
            self.place_marble(i)
            self.change_player()

    def place_marble(self, val: int):
        if val % 23 == 0:
            self.scores[self.player] += val
            self.remove_marble()
        else:
            self.insert_marble(Marble(val))

    def insert_marble(self, right: Marble):
        # go to correct marble
        self.current = self.current.next

        # insert new marble
        right.prev = self.current
        right.next = self.current.next
        self.current.next.prev = right
        self.current.next = right

        # set new marble as current
        self.current = right

    def remove_marble(self):
        # go to correct marble
        for _ in range(7):
            self.current = self.current.prev

        # remove current marble and add its value to player's score
        self.scores[self.player] += self.current.val
        right = self.current.next
        self.current.prev.next = right
        right.prev = self.current.prev

        # set new marble as current
        self.current = right

    def change_player(self):
        self.player = (self.player + 1) % self.max_players

    def get_winner(self):
        return max(self.scores.values())


def part_1(players: int, limit: int) -> int:
    game = MarbleGame(players, limit)
    game.play_game()

    return game.get_winner()


def part_2(players: int, limit: int) -> int:
    return part_1(players, limit * 100)


def parse_input():
    with open("input.txt", "r") as file:
        return (int(s) for s in re.match(r"(\d+) players; last marble is worth (\d+) points", file.read()).groups())


if __name__ == "__main__":
    player_count, last_marble = parse_input()

    print(f"Part 1: The winning Elf's score is {part_1(player_count, last_marble)}.")

    print(f"Part 2: The winning Elf's score if the limit was 100 times larger is {part_2(player_count, last_marble)}.")
