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


def part1(input: str) -> int:
    player_count, last_marble = parse(input)

    return play_game(player_count, last_marble)


def part2(input: str) -> int:
    player_count, last_marble = parse(input)

    return play_game(player_count, last_marble * 100)


def play_game(player_count: int, limit: int) -> int:
    game = MarbleGame(player_count, limit)
    game.play_game()

    return game.get_winner()


def parse(input):
    return (int(s) for s in re.match(r"(\d+) players; last marble is worth (\d+) points", input).groups())
