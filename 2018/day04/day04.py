from datetime import datetime
from collections import defaultdict
import re
import numpy as np


class Event:
    def __init__(self, date: datetime, event: str):
        self.date = date
        self.event = event


def part_1(sleep_count: dict, guard_sleeps: dict) -> int:
    longest_sleeper = max(sleep_count.keys(), key=lambda k: sleep_count[k])

    return longest_sleeper * np.argmax(guard_sleeps[longest_sleeper])


def part_2(guard_sleeps: dict) -> int:
    chosen_guard = None
    chosen_minute = None
    max_sleep = 0
    for guard_id, hour in guard_sleeps.items():
        most_frequent, minute = hour.max(), np.argmax(hour)
        if most_frequent > max_sleep:
            max_sleep = most_frequent
            chosen_guard = guard_id
            chosen_minute = minute

    return chosen_guard * chosen_minute


def process_data(events: list) -> tuple:
    # tracks total time asleep
    sleep_count = defaultdict(int)
    # tracks time asleep for guide
    guard_sleeps = defaultdict(lambda: np.zeros(60))

    guard_id = None
    sleep_start = None

    for event in events:
        if event.event.startswith("falls asleep"):
            sleep_start = event.date
        elif event.event.startswith("wakes up"):
            sleep_count[guard_id] += (event.date.minute - sleep_start.minute)
            guard_sleeps[guard_id][sleep_start.minute:event.date.minute] += 1
            #for m in range(sleep_start.minute, event.date.minute + 1):
            #    guard_sleeps[guard_id][m] += 1
        else:
            guard_id = int(re.search("(\d+)", event.event).group(0))

    return sleep_count, guard_sleeps


def parse_input():
    with open("input.txt", "r") as file:
        events = []
        for line in file.read().splitlines():
            date = datetime.strptime(line[1:17], "%Y-%m-%d %H:%M")
            events.append(Event(date, line[19:]))

        return sorted(events, key=lambda e: e.date)


if __name__ == "__main__":
    event_list = parse_input()
    guard_sum, guard_distribution = process_data(event_list)

    print(f"Part 1: The id of the guard who sleeps the most multiplied by the minute they sleep the most "
          f"is {part_1(guard_sum, guard_distribution)}.")

    print(f"Part 2: The id of the guard who is most frequently asleep at the same minute multiplied by "
          f"the minute they are asleep the most at is {part_2(guard_distribution)}.")
