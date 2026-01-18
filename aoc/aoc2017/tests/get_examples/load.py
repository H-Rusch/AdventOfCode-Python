import os
from pathlib import Path


def load_example(filename: str):
    path = Path(os.path.dirname(__file__), "../../examples", filename).resolve()

    with open(path) as file:
        return file.read()
