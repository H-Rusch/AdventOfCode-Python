from dataclasses import dataclass
from argparse import ArgumentParser

import importlib
from types import ModuleType
from datetime import datetime

from get_inputs.load_input import load_input


VIABLE_EVENTS = [2017, 2018, 2019, 2020, 2021, 2024]
VIABLE_DAYS = range(1, 26)


@dataclass
class Arguments:
    pass


def main():
    arguments = parse_arguments()
    puzzle_input = load_input(arguments.year, arguments.day)
    module = import_module(arguments.year, arguments.day)
    print(f"{arguments.year} Day {arguments.day}:")
    perform_parts(module, puzzle_input)


def parse_arguments() -> Arguments:
    arguments = Arguments()
    parser = create_arg_parser()
    parser.parse_args(namespace=arguments)

    return arguments


def create_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="Advent of Code Python",
        description="This program solves the Advent of Code event. Inputs are downloaded automatically by the program.",
    )
    parser.add_argument(
        "year",
        type=int,
        choices=VIABLE_EVENTS,
        help="The event you want to run this program for.",
    )
    parser.add_argument(
        "day",
        type=int,
        choices=VIABLE_DAYS,
        help="The day in the given year to be run.",
    )

    return parser


def import_module(year: int, day: int) -> ModuleType:
    module_name = get_module_name(year, day)
    globals()[module_name] = importlib.import_module(module_name)

    return globals()[module_name]


def get_module_name(year: int, day: int) -> str:
    return f"aoc.aoc{year}.solutions.day{day:02d}"


def perform_parts(module: ModuleType, puzzle_input: str):
    for i, part in enumerate((module.part1, module.part2)):
        start_time = datetime.now()
        result = part(puzzle_input)
        end_time = datetime.now()

        print(f"\nPart {i + 1}: {result}")
        print(f"Elapsed time: {calculate_time_diff(start_time, end_time)}")


def calculate_time_diff(start_time: datetime, end_time: datetime) -> str:
    delta = end_time - start_time

    if delta.seconds >= 1:
        minutes, seconds = divmod(delta.seconds, 60)
        ms = int(delta.microseconds / 10)

        if minutes >= 1:
            return f"{minutes}:{seconds:02d}.{ms} min"
        else:
            return f"{seconds}.{ms} s"

    if delta.microseconds >= 1000:
        ms, micros = divmod(delta.microseconds, 1000)
        return f"{ms}.{micros} ms"

    return f"{delta.microseconds} µs"


if __name__ == "__main__":
    main()
