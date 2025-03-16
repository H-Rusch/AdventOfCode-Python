from datetime import datetime
from collections import defaultdict
import re
import numpy as np


class Event:
    def __init__(self, date: datetime, event: str):
        self.date = date
        self.event = event


def part1(input: str) -> int:
    event_list = parse(input)
    sleep_count, guard_sleeps = process_data(event_list)

    longest_sleeper = max(sleep_count.keys(), key=lambda k: sleep_count[k])

    return longest_sleeper * np.argmax(guard_sleeps[longest_sleeper])


def part2(input: str) -> int:
    event_list = parse(input)
    _, guard_sleeps = process_data(event_list)

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
            sleep_count[guard_id] += event.date.minute - sleep_start.minute
            guard_sleeps[guard_id][sleep_start.minute : event.date.minute] += 1
            # for m in range(sleep_start.minute, event.date.minute + 1):
            #    guard_sleeps[guard_id][m] += 1
        else:
            guard_id = int(re.search("(\d+)", event.event).group(0))

    return sleep_count, guard_sleeps


def parse(input):
    events = []
    for line in input.splitlines():
        date = datetime.strptime(line[1:17], "%Y-%m-%d %H:%M")
        events.append(Event(date, line[19:]))

    return sorted(events, key=lambda e: e.date)
