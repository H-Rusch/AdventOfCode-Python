from pathlib import Path
import os
from . import download_input
import logging


def load_input(year: int, day: int) -> str:
    create_inputs_dir(year)

    path = input_file_path(year, day)

    if not path.is_file():
        logging.info(f"Input file for year {year} day {day} not found locally.")
        puzzle_input = download_input.download_input(year, day)
        cache_puzzle_input(path, puzzle_input)

    return read_puzzle_input(path)


def create_inputs_dir(year: int):
    path = input_dir_path(year)

    if not path.is_dir():
        path.mkdir(parents=True)


def input_dir_path(year: int) -> Path:
    cwd = os.getcwd()
    path_to_dir = f"aoc/aoc{year}/inputs"

    return Path(cwd, path_to_dir)


def input_file_path(year: int, day: int) -> Path:
    input_dir = input_dir_path(year)
    filename = build_filename(day)

    return Path(input_dir, filename)


def build_filename(day: int) -> str:
    return f"day{day:02d}.txt"


def cache_puzzle_input(path: Path, puzzle_input: str):
    with open(path, "w") as file:
        file.write(puzzle_input.rstrip())

    logging.info(f"Input saved to file at {path}")


def read_puzzle_input(path: Path) -> str:
    with open(path) as file:
        return file.read().rstrip()
